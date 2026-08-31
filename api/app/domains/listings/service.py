from uuid import UUID, uuid7

from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.core.pagination import (
    CursorPage,
    CursorPagination,
    OffsetPage,
    OffsetPagination,
)
from app.core.slug import make_slug
from app.db.uow import UnitOfWork
from app.domains.listings.api.schemas import (
    ListingCreate,
    ListingReplace,
    ListingUpdate,
)
from app.domains.listings.dto import ListingImageResult, ListingResult
from app.domains.listings.media import LISTING_IMAGE_SPEC
from app.domains.listings.models import Listing, ListingImage
from app.domains.media.service import MediaService


class ListingService:
    def __init__(
        self,
        uow: UnitOfWork,
        media_service: MediaService,
    ) -> None:
        self.uow = uow
        self.media_service = media_service

    # ─────────────────────────────────────────
    # Listings
    # ─────────────────────────────────────────

    async def create_listing(self, *, data: ListingCreate) -> ListingResult:
        async with self.uow.transaction():
            suffix = None

            while True:
                slug = make_slug(data.name, suffix)

                listing = Listing(
                    slug=slug,
                    name=data.name,
                    description=data.description,
                    price_per_night=data.price_per_night,
                    max_guests=data.max_guests,
                    images=[],
                )

                try:
                    async with self.uow.savepoint():
                        self.uow.listings.add(listing=listing)
                        await self.uow.session.flush()

                except ConflictError as exc:
                    if exc.conflict != "listings_slug":
                        raise

                    suffix = 1 if suffix is None else suffix + 1

                else:
                    break

            return self._to_listing_result(listing)

    async def list_listings_offset(
        self,
        *,
        pagination: OffsetPagination,
    ) -> OffsetPage[ListingResult]:
        page = await self.uow.listings.list_offset(pagination=pagination)

        # Rebuilding the same OffsetPage from DTO instead of ORM
        return OffsetPage(
            items=[self._to_listing_result(listing) for listing in page.items],
            has_next=page.has_next,
            total=page.total,
        )

    async def list_listings_cursor(
        self,
        *,
        pagination: CursorPagination,
    ) -> CursorPage[ListingResult]:
        page = await self.uow.listings.list_cursor(pagination=pagination)

        return CursorPage(
            items=[self._to_listing_result(listing) for listing in page.items],
            next_cursor=page.next_cursor,
        )

    async def get_listing(self, *, listing_id: UUID) -> ListingResult:
        listing = await self._get_listing(listing_id)

        return self._to_listing_result(listing)

    async def get_listing_by_slug(self, *, slug: str) -> ListingResult:
        listing = await self._get_listing_by_slug(slug)

        return self._to_listing_result(listing)

    async def update_listing(
        self,
        *,
        listing_id: UUID,
        data: ListingUpdate,
    ) -> ListingResult:
        # Partial update, exclude omitted fields
        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            raise ValidationError("No fields to update")

        async with self.uow.transaction():
            listing = await self._get_listing(listing_id)

            for field, value in update_data.items():
                setattr(listing, field, value)

            await self.uow.session.flush()

            return self._to_listing_result(listing)

    async def replace_listing(
        self,
        *,
        listing_id: UUID,
        data: ListingReplace,
    ) -> ListingResult:
        async with self.uow.transaction():
            listing = await self._get_listing(listing_id)

            # Full update
            listing.name = data.name
            listing.description = data.description
            listing.price_per_night = data.price_per_night
            listing.max_guests = data.max_guests

            await self.uow.session.flush()

            return self._to_listing_result(listing)

    async def delete_listing(self, *, listing_id: UUID) -> None:
        async with self.uow.transaction():
            listing = await self._get_listing(listing_id)

            await self.uow.listings.delete(listing=listing)

    # ─────────────────────────────────────────
    # Listing images
    # ─────────────────────────────────────────

    async def add_image(
        self,
        *,
        listing_id: UUID,
        position: int,
        content: bytes,
    ) -> ListingImageResult:
        async with self.uow.transaction():
            # Check that listing exists
            await self._get_listing(listing_id)

            image_id = uuid7()

            media = await self.media_service.add_image(
                content=content,
                storage_prefix=f"listings/{listing_id}/images",
                media_id=image_id,
                spec=LISTING_IMAGE_SPEC,
            )

            image = await self.uow.listing_images.create(
                image_id=image_id,
                listing_id=listing_id,
                position=position,
                storage_key=media.storage_key,
                content_type=media.content_type,
            )

            await self.uow.session.flush()

            return self._to_image_result(image)

    async def list_images(self, *, listing_id: UUID) -> list[ListingImageResult]:
        images = await self.uow.listing_images.list(listing_id=listing_id)

        return [self._to_image_result(image) for image in images]

    async def update_image(
        self,
        *,
        listing_id: UUID,
        image_id: UUID,
        content: bytes | None,
        position: int | None,
    ) -> ListingImageResult:
        if content is None and position is None:
            raise ValidationError("At least one field must be provided")

        async with self.uow.transaction():
            image = await self._get_image(listing_id, image_id)

            media = None

            if content is not None:
                media = await self.media_service.replace_image(
                    content=content,
                    storage_key=image.storage_key,
                    media_id=image.id,
                    spec=LISTING_IMAGE_SPEC,
                )

                image.storage_key = media.storage_key
                image.content_type = media.content_type

            if position is not None:
                image.position = position

            await self.uow.session.flush()

            return self._to_image_result(image)

    async def delete_image(
        self,
        *,
        listing_id: UUID,
        image_id: UUID,
    ) -> None:
        async with self.uow.transaction():
            image = await self._get_image(listing_id, image_id)

            await self.uow.listing_images.delete(image=image)

        await self.media_service.delete_image(storage_key=image.storage_key)

    # ─────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────

    async def _get_listing(self, listing_id: UUID) -> Listing:
        listing = await self.uow.listings.get(listing_id=listing_id)

        if listing is None:
            raise NotFoundError(f"Listing with ID {listing_id} not found")

        return listing

    async def _get_listing_by_slug(self, slug: str) -> Listing:
        listing = await self.uow.listings.get_by_slug(slug=slug)

        if listing is None:
            raise NotFoundError(f"Listing with slug {slug} not found")

        return listing

    async def _get_image(
        self,
        listing_id: UUID,
        image_id: UUID,
    ) -> ListingImage:
        # Also check that image is a sub-resource of the listing
        image = await self.uow.listing_images.get(
            listing_id=listing_id,
            image_id=image_id,
        )

        if image is None:
            raise NotFoundError(f"Listing image with ID {image_id} not found")

        return image

    def _to_image_result(self, image: ListingImage) -> ListingImageResult:
        return ListingImageResult(
            id=image.id,
            url=self.media_service.get_url(
                storage_key=image.storage_key,
            ),
            content_type=image.content_type,
            position=image.position,
            created_at=image.created_at,
            updated_at=image.updated_at,
        )

    def _to_listing_result(self, listing: Listing) -> ListingResult:
        return ListingResult(
            id=listing.id,
            slug=listing.slug,
            name=listing.name,
            description=listing.description,
            price_per_night=listing.price_per_night,
            max_guests=listing.max_guests,
            created_at=listing.created_at,
            updated_at=listing.updated_at,
            images=[self._to_image_result(image) for image in listing.images],
        )

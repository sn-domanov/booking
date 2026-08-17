from collections.abc import Sequence
from uuid import UUID, uuid7

from app.core.exceptions import NotFoundError, ValidationError
from app.db.uow import UnitOfWork
from app.domains.listings.api.schemas import (
    ListingCreate,
    ListingReplace,
    ListingUpdate,
)
from app.domains.listings.dto import ListingImageResult
from app.domains.listings.media import LISTING_IMAGE_SPEC
from app.domains.listings.models import Listing
from app.domains.media.service import MediaService


class ListingService:
    def __init__(
        self,
        uow: UnitOfWork,
        media_service: MediaService,
    ):
        self.uow = uow
        self.media_service = media_service

    # ─────────────────────────────────────────
    # Listings
    # ─────────────────────────────────────────

    async def _get_listing(self, listing_id: UUID) -> Listing:
        listing = await self.uow.listings.get(listing_id=listing_id)

        if listing is None:
            raise NotFoundError(f"Listing with ID {listing_id} not found")

        return listing

    async def create_listing(self, *, data: ListingCreate) -> Listing:
        async with self.uow.transaction():
            listing = Listing(
                name=data.name,
                description=data.description,
                price_per_night=data.price_per_night,
                max_guests=data.max_guests,
            )

            self.uow.listings.add(listing=listing)

            return listing

    async def list_listings(self) -> Sequence[Listing]:
        return await self.uow.listings.list()

    async def get_listing(self, *, listing_id: UUID) -> Listing:
        return await self._get_listing(listing_id)

    async def update_listing(
        self,
        *,
        listing_id: UUID,
        data: ListingUpdate,
    ) -> Listing:
        # Partial update, exclude omitted fields
        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            raise ValidationError("No fields to update")

        async with self.uow.transaction():
            listing = await self._get_listing(listing_id)

            for field, value in update_data.items():
                setattr(listing, field, value)

            return listing

    async def replace_listing(
        self,
        *,
        listing_id: UUID,
        data: ListingReplace,
    ) -> Listing:
        async with self.uow.transaction():
            listing = await self._get_listing(listing_id)

            # Full update
            listing.name = data.name
            listing.description = data.description
            listing.price_per_night = data.price_per_night
            listing.max_guests = data.max_guests

            return listing

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
        image_position: int,
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
                position=image_position,
                storage_key=media.storage_key,
                content_type=media.content_type,
            )

        return ListingImageResult(
            id=image.id,
            url=media.url,
            content_type=image.content_type,
            position=image.position,
            created_at=image.created_at,
            updated_at=image.updated_at,
        )

    async def list_images(self, *, listing_id: UUID) -> list[ListingImageResult]:
        images = await self.uow.listing_images.list(listing_id=listing_id)

        return [
            ListingImageResult(
                id=image.id,
                url=self.media_service.get_url(
                    storage_key=image.storage_key,
                ),
                content_type=image.content_type,
                position=image.position,
                created_at=image.created_at,
                updated_at=image.updated_at,
            )
            for image in images
        ]

    async def delete_image(
        self,
        *,
        listing_id: UUID,
        image_id: UUID,
    ) -> None:
        async with self.uow.transaction():
            # Also check that image is a sub-resource of the listing
            image = await self.uow.listing_images.get(
                listing_id=listing_id,
                image_id=image_id,
            )

            if image is None:
                raise NotFoundError("Listing image not found")

            await self.uow.listing_images.delete(image=image)

        await self.media_service.delete_image(storage_key=image.storage_key)

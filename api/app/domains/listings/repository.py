from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.core.pagination import OffsetPage, OffsetPagination
from app.db.session import AsyncSession
from app.domains.listings.models import Listing, ListingImage


class ListingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def add(self, *, listing: Listing) -> None:
        self.session.add(listing)

    async def list(self, *, pagination: OffsetPagination) -> OffsetPage[Listing]:
        filters = ()

        stmt = (
            select(Listing)
            .where(*filters)
            .options(selectinload(Listing.images))
            .order_by(
                Listing.created_at.desc(),
                Listing.id.desc(),
            )
            .offset(pagination.offset)
            .limit(pagination.limit + 1)
        )

        count_stmt = select(func.count()).select_from(Listing).where(*filters)

        result = await self.session.scalars(stmt)
        rows = list(result.all())

        total = (await self.session.execute(count_stmt)).scalar_one()

        return OffsetPage(
            items=rows[: pagination.limit],
            has_next=len(rows) > pagination.limit,
            total=total,
        )

    async def get(self, *, listing_id: UUID) -> Listing | None:
        stmt = (
            select(Listing)
            .where(Listing.id == listing_id)
            .options(selectinload(Listing.images))
        )
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def delete(self, *, listing: Listing) -> None:
        await self.session.delete(listing)


class ListingImageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        *,
        image_id: UUID,
        listing_id: UUID,
        storage_key: str,
        content_type: str,
        position: int,
    ) -> ListingImage:
        image = ListingImage(
            id=image_id,
            listing_id=listing_id,
            storage_key=storage_key,
            content_type=content_type,
            position=position,
        )

        self.session.add(image)

        return image

    async def list(self, *, listing_id: UUID) -> Sequence[ListingImage]:
        stmt = (
            select(ListingImage)
            .where(ListingImage.listing_id == listing_id)
            # Position is unique per listing, no tie-breaker
            .order_by(ListingImage.position)
        )
        result = await self.session.scalars(stmt)

        return result.all()

    async def get(
        self,
        *,
        listing_id: UUID,
        image_id: UUID,
    ) -> ListingImage | None:
        stmt = select(ListingImage).where(
            ListingImage.id == image_id,
            ListingImage.listing_id == listing_id,
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def delete(self, *, image: ListingImage) -> None:
        await self.session.delete(image)

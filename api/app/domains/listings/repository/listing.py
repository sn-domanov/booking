from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.core.pagination import (
    CursorPage,
    CursorPagination,
    OffsetPage,
    OffsetPagination,
    decode_cursor,
    encode_cursor,
)
from app.db.session import AsyncSession
from app.domains.listings.models import Listing
from app.domains.listings.repository.cursor import ListingCursor


class ListingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def add(self, *, listing: Listing) -> None:
        self.session.add(listing)

    async def list_offset(self, *, pagination: OffsetPagination) -> OffsetPage[Listing]:
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
        items = list(result.all())

        total = (await self.session.execute(count_stmt)).scalar_one()

        return OffsetPage(
            items=items[: pagination.limit],
            has_next=len(items) > pagination.limit,
            total=total,
        )

    async def list_cursor(
        self,
        *,
        pagination: CursorPagination,
    ) -> CursorPage[Listing]:
        cursor = (
            ListingCursor.from_payload(decode_cursor(pagination.cursor))
            if pagination.cursor
            else None
        )

        stmt = (
            select(Listing)
            .options(selectinload(Listing.images))
            .order_by(
                Listing.created_at.desc(),
                Listing.id.desc(),
            )
            .limit(pagination.limit + 1)
        )

        if cursor:
            stmt = stmt.where(
                (Listing.created_at < cursor.created_at)
                | ((Listing.created_at == cursor.created_at) & (Listing.id < cursor.id))
            )

        result = await self.session.scalars(stmt)
        items = list(result.all())

        has_next = len(items) > pagination.limit
        items = items[: pagination.limit]

        next_cursor = None

        if has_next:
            last = items[-1]

            next_cursor = encode_cursor(
                ListingCursor(
                    created_at=last.created_at,
                    id=last.id,
                ).to_payload()
            )

        return CursorPage(
            items=items,
            next_cursor=next_cursor,
        )

    async def get(self, *, listing_id: UUID) -> Listing | None:
        stmt = (
            select(Listing)
            .where(Listing.id == listing_id)
            .options(selectinload(Listing.images))
        )
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_slug(self, *, slug: str) -> Listing | None:
        stmt = (
            select(Listing)
            .where(Listing.slug == slug)
            .options(selectinload(Listing.images))
        )
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def delete(self, *, listing: Listing) -> None:
        await self.session.delete(listing)

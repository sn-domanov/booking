from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select

from app.db.session import AsyncSession
from app.domains.listings.models import Listing


class ListingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, *, listing: Listing) -> None:
        self.session.add(listing)

    # TODO add pagination
    async def list(self) -> Sequence[Listing]:
        stmt = select(Listing).order_by(Listing.created_at.desc(), Listing.id.desc())
        result = await self.session.scalars(stmt)

        return result.all()

    async def get(self, *, listing_id: UUID) -> Listing | None:
        stmt = select(Listing).where(Listing.id == listing_id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def delete(self, *, listing: Listing) -> None:
        await self.session.delete(listing)

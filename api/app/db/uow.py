from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.listings.repository import ListingImageRepository, ListingRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.listings = ListingRepository(session)
        self.listing_images = ListingImageRepository(session)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[UnitOfWork]:
        try:
            yield self
            # TODO translate database errors
            await self.commit()
        except Exception:
            await self.rollback()
            raise

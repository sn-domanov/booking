from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.exceptions import raise_from_database_error
from app.domains.listings.repository.constraints import (
    CONSTRAINT_MAP as LISTINGS_CONSTRAINT_MAP,
)
from app.domains.listings.repository.listing import ListingRepository
from app.domains.listings.repository.listing_image import ListingImageRepository

DATABASE_CONSTRAINT_MAP = {
    **LISTINGS_CONSTRAINT_MAP,
}


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
            await self.commit()

        except DBAPIError as exc:
            await self.rollback()

            raise_from_database_error(
                exc,
                DATABASE_CONSTRAINT_MAP,
            )

        except Exception:
            await self.rollback()
            raise

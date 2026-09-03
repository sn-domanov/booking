from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.exceptions import raise_from_database_error
from app.db.session import session_factory
from app.domains.auth.repository import RefreshTokenRepository
from app.domains.listings.repository.constraints import (
    CONSTRAINT_MAP as LISTINGS_CONSTRAINT_MAP,
)
from app.domains.listings.repository.listing import ListingRepository
from app.domains.listings.repository.listing_image import ListingImageRepository
from app.domains.users.repository import UserRepository

DATABASE_CONSTRAINT_MAP = {
    **LISTINGS_CONSTRAINT_MAP,
}


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.listings = ListingRepository(session)
        self.listing_images = ListingImageRepository(session)
        self.users = UserRepository(session)
        self.refresh_tokens = RefreshTokenRepository(session)

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

            # Translate to an application exception for the global API handler
            raise_from_database_error(
                exc,
                DATABASE_CONSTRAINT_MAP,
            )

        except Exception:
            await self.rollback()
            raise

    @asynccontextmanager
    async def savepoint(self) -> AsyncGenerator[None]:
        try:
            async with self.session.begin_nested():
                yield

        except DBAPIError as exc:
            # Translate to an application exception so the service can handle it
            raise_from_database_error(
                exc,
                DATABASE_CONSTRAINT_MAP,
            )


@asynccontextmanager
async def create_uow() -> AsyncGenerator[UnitOfWork]:
    async with session_factory() as session:
        yield UnitOfWork(session)

from collections.abc import Sequence
from uuid import UUID

# TODO introduce UoW pattern
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.domains.listings.api.schemas import (
    ListingCreate,
    ListingReplace,
    ListingUpdate,
)
from app.domains.listings.models import Listing

from .repository import ListingRepository


# TODO add core.exceptions
class ListingNotFound(Exception): ...


class ListingService:
    def __init__(
        self,
        settings: Settings,
        repository: ListingRepository,
        session: AsyncSession,
    ):
        self.settings = settings
        self.repository = repository
        self.session = session

    async def create(self, *, data: ListingCreate) -> Listing:
        listing = Listing(
            name=data.name,
            description=data.description,
            price_per_night=data.price_per_night,
            max_guests=data.max_guests,
        )

        self.repository.add(listing=listing)

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return listing

    async def list(self) -> Sequence[Listing]:
        return await self.repository.list()

    async def get(self, *, listing_id: UUID) -> Listing:
        listing = await self.repository.get(listing_id=listing_id)

        if listing is None:
            raise ListingNotFound(f"Listing with ID {listing_id} not found")

        return listing

    async def update(
        self,
        *,
        listing_id: UUID,
        data: ListingUpdate,
    ) -> Listing:
        listing = await self.repository.get(listing_id=listing_id)

        if listing is None:
            raise ListingNotFound(f"Listing with ID {listing_id} not found")

        # Partial update, exclude omitted fields
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(listing, field, value)

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return listing

    async def replace(
        self,
        *,
        listing_id: UUID,
        data: ListingReplace,
    ) -> Listing:
        listing = await self.repository.get(listing_id=listing_id)

        if listing is None:
            raise ListingNotFound(f"Listing with ID {listing_id} not found")

        # Full update
        listing.name = data.name
        listing.description = data.description
        listing.price_per_night = data.price_per_night
        listing.max_guests = data.max_guests

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return listing

    async def delete(self, *, listing_id: UUID) -> None:
        listing = await self.repository.get(listing_id=listing_id)

        if listing is None:
            raise ListingNotFound(f"Listing with ID {listing_id} not found")

        await self.repository.delete(listing=listing)

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

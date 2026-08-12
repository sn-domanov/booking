from collections.abc import Sequence
from uuid import UUID

from app.core.config import Settings
from app.db.uow import UnitOfWork
from app.domains.listings.api.schemas import (
    ListingCreate,
    ListingReplace,
    ListingUpdate,
)
from app.domains.listings.models import Listing


# TODO add core.exceptions
class ListingNotFoundError(Exception): ...


class ListingService:
    def __init__(
        self,
        settings: Settings,
        uow: UnitOfWork,
    ):
        self.settings = settings
        self.uow = uow

    async def _get_listing(self, listing_id: UUID) -> Listing:
        listing = await self.uow.listings.get(listing_id=listing_id)

        if listing is None:
            raise ListingNotFoundError(f"Listing with ID {listing_id} not found")

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

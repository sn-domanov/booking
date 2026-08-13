from app.db.uow import UnitOfWork
from app.domains.listings.models import Listing
from tests.factories.listings import listing_factory


async def create_listing(uow: UnitOfWork, **overrides) -> Listing:
    listing = listing_factory(**overrides)

    async with uow.transaction():
        uow.listings.add(listing=listing)

    return listing

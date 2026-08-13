from datetime import datetime
from decimal import Decimal

from app.domains.listings.models import Listing


def listing_factory(
    *,
    name: str = "Test Listing",
    description: str = "A test listing",
    price_per_night: Decimal = Decimal("100.00"),
    max_guests: int = 2,
    created_at: datetime | None = None,
    updated_at: datetime | None = None,
) -> Listing:
    return Listing(
        name=name,
        description=description,
        price_per_night=price_per_night,
        max_guests=max_guests,
        created_at=created_at,
        updated_at=updated_at,
    )

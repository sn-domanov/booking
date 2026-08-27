from datetime import datetime
from decimal import Decimal

from app.core.slug import make_slug
from app.domains.listings.models import Listing


def listing_factory(
    *,
    name: str = "Test Listing",
    slug: str | None = None,
    description: str = "A test listing",
    price_per_night: Decimal = Decimal("100.00"),
    max_guests: int = 2,
    created_at: datetime | None = None,
    updated_at: datetime | None = None,
) -> Listing:
    return Listing(
        name=name,
        slug=make_slug(name) if slug is None else slug,
        description=description,
        price_per_night=price_per_night,
        max_guests=max_guests,
        created_at=created_at,
        updated_at=updated_at,
    )

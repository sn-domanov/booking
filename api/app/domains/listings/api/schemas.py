from datetime import datetime
from uuid import UUID

from app.api.schemas import ApiSchema
from app.domains.listings.api.types import (
    ListingDescription,
    ListingName,
    MaxGuests,
    PricePerNight,
)


class ListingCreate(ApiSchema):
    name: ListingName
    description: ListingDescription
    price_per_night: PricePerNight
    max_guests: MaxGuests


class ListingUpdate(ApiSchema):
    name: ListingName | None = None
    description: ListingDescription | None = None
    price_per_night: PricePerNight | None = None
    max_guests: MaxGuests | None = None


class ListingReplace(ApiSchema):
    name: ListingName
    description: ListingDescription
    price_per_night: PricePerNight
    max_guests: MaxGuests


class ListingResponse(ApiSchema):
    id: UUID
    name: ListingName
    description: ListingDescription
    price_per_night: PricePerNight
    max_guests: MaxGuests
    created_at: datetime
    updated_at: datetime

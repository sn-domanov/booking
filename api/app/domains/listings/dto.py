from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ListingImageResult:
    id: UUID
    url: str
    content_type: str
    position: int
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class ListingResult:
    id: UUID
    slug: str
    name: str
    description: str
    price_per_night: Decimal
    max_guests: int
    created_at: datetime
    updated_at: datetime
    images: list[ListingImageResult]

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ListingImageResult:
    id: UUID
    url: str
    content_type: str
    position: int
    created_at: datetime
    updated_at: datetime

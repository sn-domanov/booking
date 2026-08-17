from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class MediaObject:
    id: UUID
    storage_key: str
    url: str
    content_type: str

from datetime import datetime
from uuid import UUID

from app.api.schemas import ApiSchema
from app.domains.listings.api.images.types import ContentType, ImagePosition


class ListingImageResponse(ApiSchema):
    id: UUID
    url: str
    content_type: ContentType
    position: ImagePosition
    created_at: datetime
    updated_at: datetime

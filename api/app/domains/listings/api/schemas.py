from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import Field, field_validator

from app.api.schemas import ApiSchema


class ListingCreate(ApiSchema):
    name: str
    description: str
    price_per_night: Decimal = Field(gt=0)
    max_guests: int = Field(gt=0)

    # TODO add core.normalization
    @field_validator("name", "description")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        return value.strip()


class ListingUpdate(ApiSchema):
    name: str | None = None
    description: str | None = None
    price_per_night: Decimal | None = None
    max_guests: int | None = None


class ListingReplace(ApiSchema):
    name: str
    description: str
    price_per_night: Decimal
    max_guests: int


class ListingResponse(ApiSchema):
    id: UUID
    name: str
    description: str
    price_per_night: Decimal = Field(examples=[Decimal("129.99")])
    max_guests: int
    created_at: datetime
    updated_at: datetime

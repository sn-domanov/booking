from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import Field, field_validator

from app.api.schemas import ApiSchema


class ListingCreate(ApiSchema):
    name: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=5_000)
    price_per_night: Decimal = Field(gt=0, le=100_000)
    max_guests: int = Field(gt=0)

    # TODO add core.normalization
    @field_validator("name", "description", mode="before")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        return value.strip()


class ListingUpdate(ApiSchema):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1, max_length=5_000)
    price_per_night: Decimal | None = Field(default=None, gt=0, le=100_000)
    max_guests: int | None = Field(default=None, gt=0)


class ListingReplace(ApiSchema):
    name: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=5_000)
    price_per_night: Decimal = Field(gt=0, le=100_000)
    max_guests: int = Field(gt=0)


class ListingResponse(ApiSchema):
    id: UUID
    name: str
    description: str
    price_per_night: Decimal = Field(examples=[Decimal("129.99")])
    max_guests: int
    created_at: datetime
    updated_at: datetime

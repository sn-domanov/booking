from typing import Literal, Self, TypeVar

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

from app.core.exceptions import ValidationError

T = TypeVar("T")


class ApiSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class PaginationQuery(ApiSchema):
    pagination: Literal["offset", "cursor"] = "offset"
    limit: int = Field(default=20, ge=1, le=100)
    offset: int | None = Field(default=None, ge=0)
    cursor: str | None = None

    @model_validator(mode="after")
    def validate_pagination(self) -> Self:
        if self.offset is not None and self.cursor is not None:
            raise ValidationError("offset and cursor cannot be used together")

        return self


# class OffsetPaginationQuery(BaseModel):
#     limit: int = Field(default=20, ge=1, le=100)
#     offset: int = Field(default=0, ge=0)


# class CursorPaginationQuery(BaseModel):
#     limit: int = Field(default=20, ge=1, le=100)
#     cursor: str | None = None


class OffsetPageResponse[T](ApiSchema):
    items: list[T]
    has_next: bool
    total: int


class CursorPageResponse[T](ApiSchema):
    items: list[T]
    next_cursor: str | None

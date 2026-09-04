from datetime import datetime
from uuid import UUID

from pydantic import EmailStr

from app.api.schemas import ApiSchema
from app.core.types import (
    NormalizedDisplayName,
    NormalizedEmail,
    PasswordInput,
)


class UserCreate(ApiSchema):
    email: NormalizedEmail
    password: PasswordInput
    display_name: NormalizedDisplayName


class UserResponse(ApiSchema):
    id: UUID
    display_name: str
    created_at: datetime


class CurrentUserResponse(ApiSchema):
    id: UUID
    email: EmailStr
    display_name: str
    created_at: datetime
    updated_at: datetime


class CurrentUserUpdate(ApiSchema):
    display_name: NormalizedDisplayName

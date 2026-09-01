from typing import Annotated

from pydantic import BeforeValidator, EmailStr, Field

from app.api.types import NonEmptyString


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_display_name(value: str) -> str:
    return value.strip()


NormalizedEmail = Annotated[
    EmailStr,
    BeforeValidator(normalize_email),
    Field(max_length=254),
]

PasswordInput = Annotated[
    str,
    Field(min_length=8, max_length=1024),
]

NormalizedDisplayName = Annotated[
    NonEmptyString,
    BeforeValidator(normalize_display_name),
    Field(min_length=3, max_length=150),
]

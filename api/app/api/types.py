from typing import Annotated

from pydantic import BeforeValidator, Field


def strip_string(value: str) -> str:
    return value.strip()


NonEmptyString = Annotated[
    str,
    BeforeValidator(strip_string),
    Field(min_length=1),
]

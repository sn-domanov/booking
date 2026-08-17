from typing import Annotated

from pydantic import Field

from app.api.types import NonEmptyString

ContentType = Annotated[
    NonEmptyString,
    Field(max_length=100),
]

ImagePosition = Annotated[
    int,
    Field(gt=0),
]

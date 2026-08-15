from decimal import Decimal
from typing import Annotated

from pydantic import Field

from app.api.types import NonEmptyString

ListingName = Annotated[
    NonEmptyString,
    Field(max_length=255),
]

ListingDescription = Annotated[
    NonEmptyString,
    Field(max_length=5_000),
]

PricePerNight = Annotated[
    Decimal,
    Field(gt=0, le=100_000),
]

MaxGuests = Annotated[
    int,
    Field(gt=0),
]

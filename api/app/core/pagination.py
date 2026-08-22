from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class OffsetPagination:
    limit: int
    offset: int = 0


@dataclass(frozen=True, slots=True)
class OffsetPage[T]:
    items: list[T]
    has_next: bool

    # N.B. total requires expensive COUNT, avoid with large databases
    total: int

    # Optionally echo limit and offset
    # offset: int
    # limit: int

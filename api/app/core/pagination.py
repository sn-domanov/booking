import base64
import binascii
import json
from dataclasses import dataclass
from typing import Any, TypeVar

from app.core.exceptions import InvalidCursorError

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class OffsetPagination:
    limit: int
    offset: int = 0


@dataclass(frozen=True, slots=True)
class CursorPagination:
    limit: int

    # base64 encoded string
    cursor: str | None = None


@dataclass(frozen=True, slots=True)
class OffsetPage[T]:
    items: list[T]
    has_next: bool

    # N.B. total requires expensive COUNT, avoid with large databases
    total: int

    # Optionally echo limit and offset
    # offset: int
    # limit: int


@dataclass(frozen=True, slots=True)
class CursorPage[T]:
    items: list[T]
    next_cursor: str | None


def encode_cursor(value: dict[str, Any]) -> str:
    payload = json.dumps(
        value,
        separators=(",", ":"),
    ).encode()

    return base64.urlsafe_b64encode(payload).decode()


def decode_cursor(value: str) -> dict[str, Any]:
    try:
        payload = base64.urlsafe_b64decode(value)
        result = json.loads(payload)

        if not isinstance(result, dict):
            raise InvalidCursorError("Invalid cursor")

        return result

    except (
        ValueError,
        TypeError,
        binascii.Error,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise InvalidCursorError("Invalid cursor") from exc

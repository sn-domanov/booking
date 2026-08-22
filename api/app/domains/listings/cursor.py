from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self
from uuid import UUID

from app.core.exceptions import InvalidCursorError


@dataclass(frozen=True, slots=True)
class ListingCursor:
    created_at: datetime
    id: UUID

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> Self:
        try:
            return cls(
                created_at=datetime.fromisoformat(payload["created_at"]),
                id=UUID(payload["id"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise InvalidCursorError("Invalid cursor") from exc

    def to_payload(self) -> dict[str, str]:
        return {
            "created_at": self.created_at.isoformat(),
            "id": str(self.id),
        }

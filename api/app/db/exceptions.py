from collections.abc import Mapping
from dataclasses import dataclass
from typing import NoReturn

from sqlalchemy.exc import DBAPIError, IntegrityError, OperationalError

from app.core.exceptions import ApplicationError, ConflictError


@dataclass(frozen=True, slots=True)
class ConstraintConflict:
    conflict: str
    detail: str


def _get_constraint_name(exc: IntegrityError) -> str | None:
    return getattr(
        getattr(exc.orig, "diag", None),
        "constraint_name",
        None,
    )


def raise_from_database_error(
    exc: DBAPIError,
    constraint_map: Mapping[str, ConstraintConflict],
) -> NoReturn:
    if isinstance(exc, IntegrityError):
        constraint_name = _get_constraint_name(exc)

        if constraint_name is not None:
            constraint_error = constraint_map.get(constraint_name)

            if constraint_error is not None:
                raise ConflictError(
                    constraint_error.detail,
                    conflict=constraint_error.conflict,
                ) from exc

        raise ConflictError(
            "The requested operation conflicts with existing data."
        ) from exc

    if isinstance(exc, OperationalError):
        raise ApplicationError(
            "The database is currently unavailable.",
        ) from exc

    raise exc

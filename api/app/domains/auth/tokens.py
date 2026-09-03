import secrets
import uuid
from datetime import datetime
from uuid import UUID

import jwt

from app.core.config import JwtSettings
from app.core.exceptions import ExpiredTokenError, InvalidTokenError

# ─────────────────────────────────────────
# Access token
# ─────────────────────────────────────────


def create_access_token(
    *,
    user_id: UUID,
    now: datetime,
    settings: JwtSettings,
) -> str:

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + settings.access_token_ttl,
        "jti": str(uuid.uuid4()),
    }

    return jwt.encode(
        payload,
        settings.secret_key.get_secret_value(),
        settings.algorithm,
    )


def decode_access_token(token: str, settings: JwtSettings) -> uuid.UUID:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
            options={"require": ["exp", "sub"]},
        )

        return uuid.UUID(payload["sub"])

    # `UUID` raises ValueError for an invalid UUID string.
    except ValueError as err:
        raise InvalidTokenError("Invalid token") from err
    except jwt.ExpiredSignatureError as err:
        raise ExpiredTokenError("Token expired") from err
    except jwt.InvalidTokenError as err:
        raise InvalidTokenError("Invalid token") from err


# ─────────────────────────────────────────
# Refresh token
# ─────────────────────────────────────────


def create_refresh_token() -> str:
    # Using opaque refresh token instead of JWT for refresh
    token = secrets.token_urlsafe(32)

    return token

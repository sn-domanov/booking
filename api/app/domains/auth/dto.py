from dataclasses import dataclass

from app.domains.users.models import User

# ─────────────────────────────────────────
# Authentication
# ─────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class TokenPair:
    access_token: str
    refresh_token: str


@dataclass(frozen=True, slots=True)
class LoginResult:
    user: User
    tokens: TokenPair


# ─────────────────────────────────────────
# Password reset
# ─────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class PasswordResetFlow:
    token: str
    email: str
    display_name: str

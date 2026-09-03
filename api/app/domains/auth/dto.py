from dataclasses import dataclass

from app.domains.users.models import User


@dataclass(frozen=True, slots=True)
class TokenPair:
    access_token: str
    refresh_token: str


@dataclass(frozen=True, slots=True)
class LoginResult:
    user: User
    tokens: TokenPair

from pydantic import BaseModel, EmailStr

from app.api.schemas import ApiSchema
from app.core.types import NormalizedEmail, PasswordInput
from app.domains.users.api.schemas import UserResponse

# ─────────────────────────────────────────
# Authentication
# ─────────────────────────────────────────


class LoginRequest(ApiSchema):
    email: EmailStr
    password: PasswordInput


class AuthResponse(ApiSchema):
    user: UserResponse


# OAuth 2.0 token response uses snake_case field names
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ─────────────────────────────────────────
# Password reset
# ─────────────────────────────────────────


class PasswordResetRequest(ApiSchema):
    email: NormalizedEmail


class PasswordResetConfirmRequest(ApiSchema):
    token: str
    new_password: PasswordInput

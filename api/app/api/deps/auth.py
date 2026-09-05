from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from app.api.deps.database import UoWDep
from app.api.deps.settings import SettingsDep
from app.core.exceptions import AuthenticationError
from app.domains.auth.tokens import decode_access_token
from app.domains.users.models import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
    # OAuth2PasswordBearer raises a 401 immediately if there's no Authorization header
    auto_error=False,
)


# Authentication failures at the HTTP boundary are handled directly
# rather than passed through the application exception handler
def unauthorized(detail: str = "Not authenticated") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
    )


async def get_access_token(
    request: Request,
    settings: SettingsDep,
    bearer_token: str | None = Depends(oauth2_scheme),
) -> str:
    if bearer_token:
        return bearer_token

    if cookie_token := request.cookies.get(
        settings.auth.jwt.access_token_cookie_name,
    ):
        return cookie_token

    raise unauthorized()


async def get_current_user(
    uow: UoWDep,
    settings: SettingsDep,
    access_token: str = Depends(get_access_token),
) -> User:
    try:
        user_id = decode_access_token(
            access_token,
            settings.auth.jwt,
        )
    except AuthenticationError as exc:
        raise unauthorized("Could not validate credentials") from exc

    user = await uow.users.get(user_id=user_id)

    if user is None or not user.is_active:
        raise unauthorized("Could not validate credentials")

    return user


CurrentUserDep = Annotated[
    User,
    Depends(get_current_user),
]

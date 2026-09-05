from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Request,
    Response,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps.email import EmailSenderDep
from app.api.deps.settings import SettingsDep
from app.core.exceptions import InvalidRefreshTokenError
from app.domains.auth.api.cookies import delete_auth_cookies, set_auth_cookies
from app.domains.auth.api.deps import AuthServiceDep
from app.domains.auth.api.schemas import (
    AuthResponse,
    LoginRequest,
    PasswordResetConfirmRequest,
    PasswordResetRequest,
    TokenResponse,
)
from app.domains.auth.notifications.password_reset import send_password_reset_email
from app.domains.users.api.schemas import UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def token(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDep,
) -> TokenResponse:
    result = await service.login(
        # TODO: add email normalization
        email=data.username,
        password=data.password,
    )

    return TokenResponse(
        access_token=result.tokens.access_token,
        token_type="bearer",
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    response: Response,
    data: LoginRequest,
    service: AuthServiceDep,
    settings: SettingsDep,
) -> AuthResponse:
    result = await service.login(
        email=data.email,
        password=data.password,
    )

    set_auth_cookies(
        response,
        access_token=result.tokens.access_token,
        refresh_token=result.tokens.refresh_token,
        settings=settings.auth.jwt,
    )

    return AuthResponse(
        user=UserResponse.model_validate(result.user),
    )


@router.post("/refresh", status_code=status.HTTP_204_NO_CONTENT)
async def refresh(
    request: Request,
    response: Response,
    service: AuthServiceDep,
    settings: SettingsDep,
) -> None:
    refresh_token = request.cookies.get(settings.auth.jwt.refresh_token_cookie_name)

    if refresh_token is None:
        raise InvalidRefreshTokenError("Missing refresh token")

    result = await service.refresh(refresh_token)

    set_auth_cookies(
        response,
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        settings=settings.auth.jwt,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    response: Response,
    service: AuthServiceDep,
    settings: SettingsDep,
) -> None:
    refresh_token = request.cookies.get(settings.auth.jwt.refresh_token_cookie_name)

    await service.logout(refresh_token=refresh_token)

    delete_auth_cookies(response, settings.auth.jwt)


# N.B. Always return success (even if email doesn’t exist) to prevent user enumeration
@router.post("/password-reset/request", status_code=status.HTTP_202_ACCEPTED)
async def password_reset_request(
    data: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    email_sender: EmailSenderDep,
    service: AuthServiceDep,
    settings: SettingsDep,
) -> dict[str, str]:
    flow = await service.create_password_reset_flow(email=data.email)

    if flow is not None:
        background_tasks.add_task(
            send_password_reset_email,
            email_sender=email_sender,
            to_email=flow.email,
            display_name=flow.display_name,
            token=flow.token,
            frontend_base_url=settings.frontend_base_url,
        )

    return {
        "message": "If an account exists with this email, "
        "you will receive password reset instructions."
    }


@router.post("/password-reset/confirm", status_code=status.HTTP_204_NO_CONTENT)
async def password_reset_confirm(
    data: PasswordResetConfirmRequest,
    service: AuthServiceDep,
) -> None:
    await service.reset_password(
        token=data.token,
        new_password=data.new_password,
    )

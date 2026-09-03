from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps.settings import SettingsDep
from app.domains.auth.api.cookies import delete_auth_cookies, set_auth_cookies
from app.domains.auth.api.deps import AuthServiceDep
from app.domains.auth.api.schemas import (
    AuthResponse,
    LoginRequest,
    TokenResponse,
)
from app.domains.users.api.schemas import UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDep,
) -> TokenResponse:
    result = await service.login(
        # TODO: add email normalization
        email=form_data.username,
        password=form_data.password,
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
        settings=settings.jwt,
    )

    return AuthResponse(
        user=UserResponse.model_validate(result.user),
    )


@router.post("/refresh", status_code=status.HTTP_204_NO_CONTENT)
async def refresh(
    response: Response,
    refresh_token: Annotated[str, Cookie()],
    service: AuthServiceDep,
    settings: SettingsDep,
) -> None:
    result = await service.refresh(refresh_token)

    set_auth_cookies(
        response,
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        settings=settings.jwt,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    response: Response,
    service: AuthServiceDep,
    settings: SettingsDep,
) -> None:
    refresh_token = request.cookies.get(settings.jwt.refresh_token_cookie_name)

    await service.logout(refresh_token=refresh_token)

    delete_auth_cookies(response, settings.jwt)

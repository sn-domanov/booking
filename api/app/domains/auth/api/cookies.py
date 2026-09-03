from fastapi import Response

from app.core.config import JwtSettings


def set_auth_cookies(
    response: Response,
    *,
    access_token: str,
    refresh_token: str,
    settings: JwtSettings,
) -> None:
    response.set_cookie(
        key=settings.access_token_cookie_name,
        value=access_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        max_age=int(settings.access_token_ttl.total_seconds()),
        path="/",
    )

    response.set_cookie(
        key=settings.refresh_token_cookie_name,
        value=refresh_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        max_age=int(settings.refresh_token_ttl.total_seconds()),
        path="/api/v1/auth",
    )


def delete_auth_cookies(
    response: Response,
    settings: JwtSettings,
) -> None:
    response.delete_cookie(
        key=settings.access_token_cookie_name,
        path="/",
    )

    response.delete_cookie(
        key=settings.refresh_token_cookie_name,
        path="/api/v1/auth",
    )

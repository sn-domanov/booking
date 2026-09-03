from httpx import AsyncClient

from app.db.uow import UnitOfWork
from tests.helpers.users import create_user

# ─────────────────────────────────────────
# POST /api/v1/auth/logout
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 200 OK
# ─────────────────────────────────────────


async def test_logout_success(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    await create_user(
        uow,
        email="test@example.com",
        password="testpass",
    )

    # Login
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpass",
        },
    )

    assert response.status_code == 200
    assert client.cookies.get("access_token")
    assert client.cookies.get("refresh_token")

    # Logout
    response = await client.post("/api/v1/auth/logout")

    assert response.status_code == 204

    # Cookies should be deleted
    cookies = response.headers.get_list("set-cookie")

    access_cookie = next(c for c in cookies if c.startswith("access_token="))
    refresh_cookie = next(c for c in cookies if c.startswith("refresh_token="))

    assert "Max-Age=0" in access_cookie
    assert "Max-Age=0" in refresh_cookie

    assert client.cookies.get("access_token") is None
    assert client.cookies.get("refresh_token") is None


async def test_logout_revokes_refresh_token(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    await create_user(
        uow,
        email="test@example.com",
        password="testpass",
    )

    # Login
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpass",
        },
    )

    assert response.status_code == 200

    refresh_token = client.cookies.get("refresh_token")
    assert refresh_token

    # Logout
    response = await client.post("/api/v1/auth/logout")

    assert response.status_code == 204

    # The previously valid refresh token must no longer work
    response = await client.post(
        "/api/v1/auth/refresh",
        cookies={"refresh_token": refresh_token},
    )

    assert response.status_code == 401

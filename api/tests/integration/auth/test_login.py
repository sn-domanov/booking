from httpx import AsyncClient

from app.db.uow import UnitOfWork
from app.domains.users.api.schemas import UserResponse
from tests.helpers.users import create_user

# ─────────────────────────────────────────
# POST /api/v1/auth/login
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 200 OK
# ─────────────────────────────────────────


async def test_login_success(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    user = await create_user(uow, email="test@example.com", password="testpass")

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpass",
        },
    )

    assert response.status_code == 200

    cookies = response.headers.get_list("set-cookie")

    access_cookie = next(c for c in cookies if c.startswith("access_token="))
    refresh_cookie = next(c for c in cookies if c.startswith("refresh_token="))

    assert "Secure" in access_cookie
    assert "HttpOnly" in access_cookie
    assert "SameSite=lax" in access_cookie

    assert "Secure" in refresh_cookie
    assert "HttpOnly" in refresh_cookie
    assert "SameSite=lax" in refresh_cookie

    data = response.json()

    assert data["user"] is not None
    assert data["user"]["id"] == str(user.id)
    UserResponse.model_validate(data["user"])


# ─────────────────────────────────────────
# 401 Unauthorized
# ─────────────────────────────────────────


async def test_login_invalid_password(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    await create_user(uow, email="test@example.com", password="testpass")

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrong-password",
        },
    )
    assert response.status_code == 401

    data = response.json()

    assert "email or password" in data["detail"].lower()


async def test_login_unknown_user(
    client: AsyncClient,
) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "missing@example.com",
            "password": "secret123",
        },
    )
    assert response.status_code == 401

    data = response.json()

    assert "email or password" in data["detail"].lower()

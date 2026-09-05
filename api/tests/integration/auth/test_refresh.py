from httpx import AsyncClient

from app.db.uow import UnitOfWork
from tests.helpers.users import login_as

# ─────────────────────────────────────────
# POST /api/v1/auth/refresh
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 204 No Content
# ─────────────────────────────────────────


async def test_refresh_success(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    await login_as(
        client,
        uow,
        email="test@example.com",
        password="testpass",
    )

    old_access_token = client.cookies.get("access_token")
    old_refresh_token = client.cookies.get("refresh_token")

    assert old_access_token
    assert old_refresh_token

    # Refresh.
    response = await client.post(
        "/api/v1/auth/refresh",
    )

    assert response.status_code == 204

    new_access_token = client.cookies.get("access_token")
    new_refresh_token = client.cookies.get("refresh_token")

    assert new_access_token
    assert new_refresh_token

    assert new_access_token != old_access_token
    assert new_refresh_token != old_refresh_token


# ─────────────────────────────────────────
# 401 Unauthorized
# ─────────────────────────────────────────


async def test_refresh_invalid_token(
    client: AsyncClient,
) -> None:
    response = await client.post(
        "/api/v1/auth/refresh",
        cookies={"refresh_token": "invalid-token"},
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid refresh token"


async def test_refresh_without_cookie(
    client: AsyncClient,
) -> None:
    response = await client.post("/api/v1/auth/refresh")

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Missing refresh token"

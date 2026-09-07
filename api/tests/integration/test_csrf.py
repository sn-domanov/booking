from httpx import AsyncClient

from app.db.uow import UnitOfWork
from tests.helpers.users import login_as

# ─────────────────────────────────────────
# GET /api/v1/csrf
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 200 OK
# ─────────────────────────────────────────


async def test_csrf_safe_request_does_not_require_token(
    client: AsyncClient,
) -> None:
    response = await client.get("/api/v1/listings")

    assert response.status_code == 200


async def test_csrf_unsafe_request_accepts_valid_token(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    await login_as(client, uow)

    response = await client.post(
        "/api/v1/auth/logout",
    )

    assert response.status_code == 204


# ─────────────────────────────────────────
# 422 Unprocessable Content (CSRFProtect)
# ─────────────────────────────────────────


async def test_csrf_unsafe_request_requires_token(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    await login_as(client, uow)

    client.headers.pop("X-CSRF-Token")

    response = await client.post(
        "/api/v1/auth/logout",
    )

    assert response.status_code == 422

    data = response.json()

    assert "X-CSRF-Token" in data["detail"]

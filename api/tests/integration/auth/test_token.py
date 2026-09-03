from httpx import AsyncClient

from app.db.uow import UnitOfWork
from tests.helpers.users import create_user

# ─────────────────────────────────────────
# POST /api/v1/auth/token
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 200 OK
# ─────────────────────────────────────────


async def test_token_success(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    await create_user(uow, email="test@example.com", password="testpass")

    response = await client.post(
        "/api/v1/auth/token",
        data={
            "username": "test@example.com",
            "password": "testpass",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


# ─────────────────────────────────────────
# 401 Unauthorized
# ─────────────────────────────────────────


async def test_token_invalid_password(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    await create_user(uow, email="test@example.com", password="testpass")

    response = await client.post(
        "/api/v1/auth/token",
        data={
            "username": "test@example.com",
            "password": "wrong-password",
        },
    )
    assert response.status_code == 401

    data = response.json()

    assert "email or password" in data["detail"].lower()


async def test_token_unknown_user(
    client: AsyncClient,
) -> None:
    response = await client.post(
        "/api/v1/auth/token",
        data={
            "username": "missing@example.com",
            "password": "secret123",
        },
    )
    assert response.status_code == 401

    data = response.json()

    assert "email or password" in data["detail"].lower()

import uuid
from datetime import datetime

from httpx import AsyncClient

from app.db.uow import UnitOfWork
from app.domains.users.api.schemas import UserResponse
from tests.helpers.users import create_user

# ─────────────────────────────────────────
# GET /api/v1/users/{user_id}
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 200 OK
# ─────────────────────────────────────────


async def test_user_get_success(client: AsyncClient, uow: UnitOfWork) -> None:
    user = await create_user(uow)

    response = await client.get(
        f"/api/v1/users/{user.id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(user.id)


async def test_user_get_response_shape(client: AsyncClient, uow: UnitOfWork) -> None:
    user = await create_user(uow)

    response = await client.get(
        f"/api/v1/users/{user.id}",
    )

    assert response.status_code == 200
    data = UserResponse.model_validate(response.json())

    # Timestamps exist + parsed correctly
    assert isinstance(data.created_at, datetime)

    # Timestamps TZ-aware
    assert data.created_at.tzinfo is not None


# ─────────────────────────────────────────
# 404 Not Found
# ─────────────────────────────────────────


async def test_user_get_not_found(client: AsyncClient) -> None:
    user_id = uuid.UUID("00000000-0000-0000-0000-000000000000")

    response = await client.get(
        f"/api/v1/users/{user_id}",
    )

    assert response.status_code == 404

    data = response.json()

    assert data["code"] == "not_found"
    assert str(user_id) not in data["detail"]

import pytest
from httpx import AsyncClient

from app.core.security import verify_password
from app.db.uow import UnitOfWork
from tests.helpers.users import login_as, set_csrf_header

# ─────────────────────────────────────────
# PATCH /api/v1/users/me/password
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 200 OK
# ─────────────────────────────────────────


async def test_change_password_success(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    user = await login_as(
        client,
        uow,
        email="test@example.com",
        password="old-password",
    )

    response = await client.patch(
        "/api/v1/users/me/password",
        json={
            "currentPassword": "old-password",
            "newPassword": "new-password",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Password changed successfully.",
    }

    user = await uow.users.get(user_id=user.id)

    assert user is not None
    assert verify_password("new-password", user.password_hash)
    assert not verify_password("old-password", user.password_hash)


async def test_change_password_revokes_refresh_tokens(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    user = await login_as(
        client,
        uow,
        email="test@example.com",
        password="old-password",
    )

    response = await client.patch(
        "/api/v1/users/me/password",
        json={
            "currentPassword": "old-password",
            "newPassword": "new-password",
        },
    )

    assert response.status_code == 200

    refresh_tokens = await uow.refresh_tokens.list_by_user_id(user_id=user.id)

    assert len(refresh_tokens) == 1
    assert refresh_tokens[0].revoked_at is not None


async def test_change_password_deletes_password_reset_tokens(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    # Login
    user = await login_as(
        client,
        uow,
        email="test@example.com",
        password="old-password",
    )

    # Request password reset
    response = await client.post(
        "/api/v1/auth/password-reset/request",
        json={
            "email": "test@example.com",
        },
    )

    assert response.status_code == 202

    # Change password
    response = await client.patch(
        "/api/v1/users/me/password",
        json={
            "currentPassword": "old-password",
            "newPassword": "new-password",
        },
    )

    assert response.status_code == 200

    password_reset_tokens = await uow.password_reset_tokens.list_by_user_id(
        user_id=user.id
    )

    assert password_reset_tokens == []


# ─────────────────────────────────────────
# 400 Bad Request
# ─────────────────────────────────────────


async def test_change_password_invalid_current_password(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    await login_as(
        client,
        uow,
        email="test@example.com",
        password="old-password",
    )

    response = await client.patch(
        "/api/v1/users/me/password",
        json={
            "currentPassword": "wrong-password",
            "newPassword": "new-password",
        },
    )

    assert response.status_code == 400


# ─────────────────────────────────────────
# 401 Unauthorized
# ─────────────────────────────────────────


async def test_change_password_unauthenticated(
    client: AsyncClient,
) -> None:
    await set_csrf_header(client)

    response = await client.patch(
        "/api/v1/users/me/password",
        json={
            "currentPassword": "old-password",
            "newPassword": "new-password",
        },
    )

    assert response.status_code == 401


# ─────────────────────────────────────────
# 422 Request Validation (Pydantic/FastAPI)
# ─────────────────────────────────────────


@pytest.mark.parametrize(
    ("field", "value", "status_code"),
    [
        ("newPassword", "a" * 7, 422),
        ("newPassword", "a" * 8, 200),
        ("newPassword", "a" * 1024, 200),
        ("newPassword", "a" * 1025, 422),
    ],
)
async def test_change_password_new_password_boundaries(
    client: AsyncClient,
    uow: UnitOfWork,
    field: str,
    value: str,
    status_code: int,
) -> None:
    await login_as(
        client,
        uow,
        email="test@example.com",
        password="old-password",
    )

    response = await client.patch(
        "/api/v1/users/me/password",
        json={
            "currentPassword": "old-password",
            field: value,
        },
    )

    assert response.status_code == status_code

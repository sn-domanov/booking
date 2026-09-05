from datetime import UTC, datetime, timedelta

from httpx import AsyncClient

from app.core.security import hash_token, verify_password
from app.db.uow import UnitOfWork
from tests.fakes.email import FakeEmailSender
from tests.helpers.users import create_user

# ─────────────────────────────────────────
# POST /api/v1/auth/password-reset/request
# ─────────────────────────────────────────


async def test_password_reset_request_sends_email(
    client: AsyncClient,
    uow: UnitOfWork,
    fake_email_sender: FakeEmailSender,
) -> None:
    user = await create_user(uow)

    response = await client.post(
        "/api/v1/auth/password-reset/request",
        json={"email": user.email},
    )

    assert response.status_code == 202

    assert len(fake_email_sender.messages) == 1

    email = fake_email_sender.messages[0]

    assert email.to == user.email


# ─────────────────────────────────────────
# 202 Accepted
# ─────────────────────────────────────────


async def test_password_reset_request_success(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    user = await create_user(uow)

    response = await client.post(
        "/api/v1/auth/password-reset/request",
        json={"email": user.email},
    )

    assert response.status_code == 202

    data = response.json()

    assert data["message"] == (
        "If an account exists with this email, "
        "you will receive password reset instructions."
    )

    token = await uow.password_reset_tokens.get_for_user(
        user_id=user.id,
    )

    assert token is not None


async def test_password_reset_request_unknown_email(
    client: AsyncClient,
) -> None:
    response = await client.post(
        "/api/v1/auth/password-reset/request",
        json={"email": "unknown@example.com"},
    )

    assert response.status_code == 202

    data = response.json()

    assert data["message"] == (
        "If an account exists with this email, "
        "you will receive password reset instructions."
    )


# ─────────────────────────────────────────
# POST /api/v1/auth/password-reset/confirm
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 204 No Content
# ─────────────────────────────────────────


async def test_password_reset_confirm_success(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    now = datetime.now(UTC)

    user = await create_user(
        uow,
        email="test@example.com",
        password="old-password",
    )

    raw_token = "test-reset-token"

    await uow.password_reset_tokens.create(
        user_id=user.id,
        token_hash=hash_token(raw_token),
        expires_at=now + timedelta(minutes=60),
    )

    response = await client.post(
        "/api/v1/auth/password-reset/confirm",
        json={
            "token": raw_token,
            "new_password": "new-password",
        },
    )

    assert response.status_code == 204

    user = await uow.users.get(user_id=user.id)

    assert user is not None
    assert verify_password("new-password", user.password_hash)
    assert not verify_password("old-password", user.password_hash)

    token = await uow.password_reset_tokens.get_by_hash(
        token_hash=hash_token(raw_token),
    )

    assert token is None


# ─────────────────────────────────────────
# 401 Unauthorized
# ─────────────────────────────────────────


async def test_password_reset_confirm_invalid_token(
    client: AsyncClient,
) -> None:
    response = await client.post(
        "/api/v1/auth/password-reset/confirm",
        json={
            "token": "invalid-token",
            "new_password": "new-password",
        },
    )

    assert response.status_code == 400


async def test_password_reset_confirm_expired_token(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    now = datetime.now(UTC)

    user = await create_user(
        uow,
        email="test@example.com",
        password="old-password",
        display_name="Test User",
    )

    raw_token = "expired-reset-token"

    await uow.password_reset_tokens.create(
        user_id=user.id,
        token_hash=hash_token(raw_token),
        expires_at=now - timedelta(seconds=1),
    )

    response = await client.post(
        "/api/v1/auth/password-reset/confirm",
        json={
            "token": raw_token,
            "new_password": "new-password",
        },
    )

    assert response.status_code == 400

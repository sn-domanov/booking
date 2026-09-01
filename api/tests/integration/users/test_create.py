import uuid

import pytest
from httpx import AsyncClient

# ─────────────────────────────────────────
# POST /api/v1/users
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 201 Created
# ─────────────────────────────────────────


async def test_user_create_success(client: AsyncClient) -> None:
    payload = {
        "email": "test@example.com",
        "display_name": "Test User",
        "password": "testpass",
    }

    response = await client.post(
        "/api/v1/users",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    # Generated fields
    assert data["id"] is not None
    uuid.UUID(data["id"])

    assert data["createdAt"] is not None


@pytest.mark.parametrize(
    ("field", "response_field", "value", "expected"),
    [
        # TODO: test once auth and `/users/me` are available for fetching user email
        # ("email", "email", " Test-email@example.com ", "test-email@example.com"),
        # ("email", "email", "TEST@EXAMPLE.COM", "test@example.com"),
        # ("email", "email", "Test.Email@Example.Com", "test.email@example.com"),
        # (
        #     "email",
        #     "email",
        #     "already.normalized@example.com",
        #     "already.normalized@example.com",
        # ),
        # ("email", "email", "\ttest@example.com\n", "test@example.com"),
        ("display_name", "displayName", " Test User ", "Test User"),
        ("display_name", "displayName", "TEST USER", "TEST USER"),
        ("display_name", "displayName", "\ttest user\n", "test user"),
    ],
)
async def test_user_create_normalizes_values(
    client: AsyncClient,
    field: str,
    response_field: str,
    value: str,
    expected: str,
) -> None:
    payload = {
        "email": "test@example.com",
        "display_name": "Test User",
        "password": "testpass",
    }
    payload[field] = value

    response = await client.post(
        "/api/v1/users",
        json=payload,
    )

    assert response.status_code == 201
    assert response.json()[response_field] == expected


@pytest.mark.parametrize(
    "field",
    ["email", "password", "display_name"],
)
async def test_user_create_rejects_missing_required_field(
    client: AsyncClient,
    field: str,
) -> None:
    payload = {
        "email": "test@example.com",
        "display_name": "Test User",
        "password": "testpass",
    }
    del payload[field]

    response = await client.post(
        "/api/v1/users",
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("field", "value", "status_code"),
    [
        ("email", "a@example.com", 201),
        ("email", "a" * 246 + "@example.com", 422),  # > 254 chars
        ("password", "a" * 8, 201),
        ("password", "a" * 1024, 201),
        ("password", "a" * 7, 422),
        ("password", "a" * 1025, 422),
        ("display_name", "abc", 201),
        ("display_name", "a" * 150, 201),
        ("display_name", " ab ", 422),  # normalizes to 2 chars
        ("display_name", " abc ", 201),  # normalizes to 3 chars
        ("display_name", "a" * 151, 422),
    ],
)
async def test_user_create_value_boundaries(
    client: AsyncClient,
    field: str,
    value: str,
    status_code: int,
) -> None:
    payload = {
        "email": "test@example.com",
        "display_name": "Test User",
        "password": "testpass",
    }
    payload[field] = value

    response = await client.post(
        "/api/v1/users",
        json=payload,
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("email", "not-an-email"),
    ],
)
async def test_user_create_rejects_invalid_values(
    client: AsyncClient,
    field: str,
    value: str,
) -> None:
    payload = {
        "email": "test@example.com",
        "display_name": "Test User",
        "password": "testpass",
    }
    payload[field] = value

    response = await client.post(
        "/api/v1/users",
        json=payload,
    )

    assert response.status_code == 422

import uuid

import pytest
from httpx import AsyncClient

from app.db.uow import UnitOfWork
from tests.helpers.listings import create_listing

# ─────────────────────────────────────────
# POST /api/v1/listings
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 201 Created
# ─────────────────────────────────────────


async def test_listing_create_success(client: AsyncClient) -> None:
    payload = {
        "name": "Test Listing",
        "description": "A test listing",
        "price_per_night": "100.00",
        "max_guests": 2,
    }

    response = await client.post(
        "/api/v1/listings",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    # Generated fields
    assert data["id"] is not None
    uuid.UUID(data["id"])

    assert data["slug"] is not None
    assert data["createdAt"] is not None
    assert data["updatedAt"] is not None


@pytest.mark.parametrize(
    ("field", "value", "expected"),
    [
        ("name", "  Test Listing  ", "Test Listing"),
        ("name", "\nTest Listing\t", "Test Listing"),
        ("description", "  A test listing  ", "A test listing"),
        ("description", "\tA test listing\n", "A test listing"),
    ],
)
async def test_listing_create_normalization(
    client: AsyncClient,
    field: str,
    value: str,
    expected: str,
) -> None:
    payload = {
        "name": value if field == "name" else "Test Listing",
        "description": value if field == "description" else "A test listing",
        "price_per_night": "100.00",
        "max_guests": 2,
    }

    response = await client.post(
        "/api/v1/listings",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data[field] == expected


async def test_create_generates_slug(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    await create_listing(uow, name="Quiet City Retreat")

    payload = {
        "name": "Quiet City Retreat",
        "description": "A peaceful city retreat.",
        "price_per_night": "100.00",
        "max_guests": 2,
    }

    response = await client.post(
        "/api/v1/listings",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["slug"] == "quiet-city-retreat-2"


# ─────────────────────────────────────────
# 422 Request Validation (Pydantic/FastAPI)
# ─────────────────────────────────────────


@pytest.mark.parametrize(
    "field",
    ["name", "description", "price_per_night", "max_guests"],
)
async def test_listing_create_rejects_missing_required_field(
    client: AsyncClient,
    field: str,
) -> None:
    payload = {
        "name": "Test Listing",
        "description": "A test listing",
        "price_per_night": "100.00",
        "max_guests": 2,
    }
    del payload[field]

    response = await client.post(
        "/api/v1/listings",
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("name", ""),
        ("name", "A" * 256),
        ("description", ""),
        ("description", "A" * 5001),
        ("price_per_night", "0"),
        ("price_per_night", "-0.01"),
        ("price_per_night", "100_000.01"),
        ("max_guests", 0),
        ("max_guests", -1),
    ],
)
async def test_listing_create_rejects_invalid_values(
    client: AsyncClient,
    field: str,
    value: str | int,
) -> None:
    payload = {
        "name": "Test Listing",
        "description": "A test listing",
        "price_per_night": "100.00",
        "max_guests": 2,
    }
    payload[field] = value

    response = await client.post(
        "/api/v1/listings",
        json=payload,
    )

    assert response.status_code == 422

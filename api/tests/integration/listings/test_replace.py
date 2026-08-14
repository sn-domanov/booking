import uuid

import pytest
from httpx import AsyncClient

from app.db.uow import UnitOfWork
from tests.helpers.listings import create_listing

# ─────────────────────────────────────────
# PUT /api/v1/listings/{listing_id}
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 200 OK
# ─────────────────────────────────────────


async def test_listing_replace_success(client: AsyncClient, uow: UnitOfWork) -> None:
    listing = await create_listing(uow)

    payload = {
        "name": "Replace Listing",
        "description": "A replace listing",
        "price_per_night": 199.99,
        "max_guests": 4,
    }

    put_response = await client.put(
        f"/api/v1/listings/{listing.id}",
        json=payload,
    )

    assert put_response.status_code == 200
    assert put_response.json()["id"] == str(listing.id)
    assert put_response.json()["name"] == "Replace Listing"

    get_response = await client.get(
        f"/api/v1/listings/{listing.id}",
    )

    assert get_response.status_code == 200
    assert get_response.json()["id"] == str(listing.id)
    assert get_response.json()["name"] == "Replace Listing"
    assert get_response.json()["description"] == "A replace listing"
    assert get_response.json()["pricePerNight"] == "199.99"
    assert get_response.json()["maxGuests"] == 4


# ─────────────────────────────────────────
# 404 Not Found
# ─────────────────────────────────────────


async def test_listing_replace_not_found(client: AsyncClient) -> None:
    listing_id = uuid.UUID("00000000-0000-0000-0000-000000000000")

    payload = {
        "name": "Replace Listing",
        "description": "A replace listing",
        "price_per_night": 199.99,
        "max_guests": 4,
    }

    response = await client.put(
        f"/api/v1/listings/{listing_id}",
        json=payload,
    )

    assert response.status_code == 404

    data = response.json()

    assert data["code"] == "not_found"
    assert str(listing_id) in data["detail"]


# ─────────────────────────────────────────
# 422 Request Validation (Pydantic/FastAPI)
# ─────────────────────────────────────────


@pytest.mark.parametrize(
    "field",
    ["name", "description", "price_per_night", "max_guests"],
)
async def test_listing_replace_rejects_missing_required_field(
    client: AsyncClient,
    uow: UnitOfWork,
    field: str,
) -> None:
    listing = await create_listing(uow)

    payload = {
        "name": "Replace Listing",
        "description": "A replace listing",
        "price_per_night": "200.00",
        "max_guests": 4,
    }
    del payload[field]

    response = await client.put(
        f"/api/v1/listings/{listing.id}",
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
async def test_listing_replace_rejects_invalid_values(
    client: AsyncClient,
    uow: UnitOfWork,
    field: str,
    value: str | int,
) -> None:
    listing = await create_listing(uow)

    payload = {
        "name": "Replace Listing",
        "description": "A replace listing",
        "price_per_night": "200.00",
        "max_guests": 4,
    }
    payload[field] = value

    response = await client.put(
        f"/api/v1/listings/{listing.id}",
        json=payload,
    )

    assert response.status_code == 422

import uuid

import pytest
from httpx import AsyncClient

from app.db.uow import UnitOfWork
from tests.helpers.listings import create_listing

# ─────────────────────────────────────────
# PATCH /api/v1/listings/{listing_id}
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 200 OK
# ─────────────────────────────────────────


async def test_listing_update_success(client: AsyncClient, uow: UnitOfWork) -> None:
    listing = await create_listing(uow)

    patch_response = await client.patch(
        f"/api/v1/listings/{listing.id}",
        json={"name": "Updated name"},
    )

    assert patch_response.status_code == 200
    assert patch_response.json()["id"] == str(listing.id)
    assert patch_response.json()["name"] == "Updated name"

    get_response = await client.get(
        f"/api/v1/listings/{listing.id}",
    )

    assert get_response.status_code == 200
    assert get_response.json()["id"] == str(listing.id)
    assert get_response.json()["name"] == "Updated name"


async def test_listing_update_changes_only_provided_fields(
    client: AsyncClient, uow: UnitOfWork
) -> None:
    listing = await create_listing(
        uow,
        name="Original name",
        description="Original description",
        price_per_night=99.99,
        max_guests=2,
    )

    response = await client.patch(
        f"/api/v1/listings/{listing.id}",
        json={"name": "Updated name"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated name"
    assert data["description"] == "Original description"
    assert data["pricePerNight"] == "99.99"
    assert data["maxGuests"] == 2


# ─────────────────────────────────────────
# 404 Not Found
# ─────────────────────────────────────────


async def test_listing_update_not_found(client: AsyncClient) -> None:
    listing_id = uuid.UUID("00000000-0000-0000-0000-000000000000")

    response = await client.patch(
        f"/api/v1/listings/{listing_id}",
        json={"name": "Updated name"},
    )

    assert response.status_code == 404

    data = response.json()

    assert data["code"] == "not_found"
    assert str(listing_id) in data["detail"]


# ─────────────────────────────────────────
# 422 Request Validation (Pydantic/FastAPI)
# ─────────────────────────────────────────


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
async def test_listing_update_rejects_invalid_values(
    client: AsyncClient,
    uow: UnitOfWork,
    field: str,
    value: str | int,
) -> None:
    listing = await create_listing(uow)

    response = await client.patch(
        f"/api/v1/listings/{listing.id}",
        json={field: value},
    )

    assert response.status_code == 422


# ─────────────────────────────────────────
# 422 Application Validation
# ─────────────────────────────────────────


async def test_listing_update_rejects_empty_update(
    client: AsyncClient, uow: UnitOfWork
) -> None:
    listing = await create_listing(uow)

    response = await client.patch(
        f"/api/v1/listings/{listing.id}",
        json={},
    )

    assert response.status_code == 422

    data = response.json()

    assert data["code"] == "validation_error"
    assert data["detail"] == "No fields to update"

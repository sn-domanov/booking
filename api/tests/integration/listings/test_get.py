import uuid
from datetime import datetime

from httpx import AsyncClient

from app.db.uow import UnitOfWork
from app.domains.listings.api.schemas import ListingResponse
from tests.helpers.listings import create_listing

# ─────────────────────────────────────────
# GET /api/v1/listings/{listing_id}
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 200 OK
# ─────────────────────────────────────────


async def test_listing_get_success(client: AsyncClient, uow: UnitOfWork) -> None:
    listing = await create_listing(uow)

    response = await client.get(
        f"/api/v1/listings/{listing.id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(listing.id)


async def test_listing_get_response_shape(client: AsyncClient, uow: UnitOfWork) -> None:
    listing = await create_listing(uow)

    response = await client.get(
        f"/api/v1/listings/{listing.id}",
    )

    assert response.status_code == 200
    data = ListingResponse.model_validate(response.json())  # or manual field assertions

    # Timestamps exist + parsed correctly
    assert isinstance(data.created_at, datetime)
    assert isinstance(data.updated_at, datetime)

    # Timestamps TZ-aware
    assert data.created_at.tzinfo is not None
    assert data.updated_at.tzinfo is not None


# ─────────────────────────────────────────
# 404 Not Found
# ─────────────────────────────────────────


async def test_listing_get_not_found(client: AsyncClient) -> None:
    listing_id = uuid.UUID("00000000-0000-0000-0000-000000000000")

    response = await client.get(
        f"/api/v1/listings/{listing_id}",
    )

    assert response.status_code == 404

    data = response.json()

    assert data["code"] == "not_found"
    assert str(listing_id) in data["detail"]


# ─────────────────────────────────────────
# GET /api/v1/listings/by-slug/{slug}
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 200 OK
# ─────────────────────────────────────────


async def test_listing_get_by_slug_success(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    listing = await create_listing(uow)

    response = await client.get(
        f"/api/v1/listings/by-slug/{listing.slug}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["slug"] == listing.slug


async def test_listing_get_by_slug_response_shape(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    listing = await create_listing(uow)

    response = await client.get(
        f"/api/v1/listings/by-slug/{listing.slug}",
    )

    assert response.status_code == 200
    data = ListingResponse.model_validate(response.json())

    # Timestamps exist + parsed correctly
    assert isinstance(data.created_at, datetime)
    assert isinstance(data.updated_at, datetime)

    # Timestamps TZ-aware
    assert data.created_at.tzinfo is not None
    assert data.updated_at.tzinfo is not None


# ─────────────────────────────────────────
# 404 Not Found
# ─────────────────────────────────────────


async def test_listing_get_by_slug_not_found(client: AsyncClient) -> None:
    slug = "does-not-exist"

    response = await client.get(
        f"/api/v1/listings/by-slug/{slug}",
    )

    assert response.status_code == 404

    data = response.json()

    assert data["code"] == "not_found"
    assert slug in data["detail"]

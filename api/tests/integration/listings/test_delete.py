import uuid

from httpx import AsyncClient

from app.db.uow import UnitOfWork
from tests.helpers.listings import create_listing

# ─────────────────────────────────────────
# DELETE /api/v1/listings
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 204 No Content
# ─────────────────────────────────────────


async def test_listing_delete_success(client: AsyncClient, uow: UnitOfWork) -> None:
    listing = await create_listing(uow)

    delete_response = await client.delete(
        f"/api/v1/listings/{listing.id}",
    )

    assert delete_response.status_code == 204

    get_response = await client.get(
        f"/api/v1/listings/{listing.id}",
    )

    assert get_response.status_code == 404


# ─────────────────────────────────────────
# 404 Not Found
# ─────────────────────────────────────────


async def test_listing_delete_not_found(client: AsyncClient) -> None:
    listing_id = uuid.UUID("00000000-0000-0000-0000-000000000000")

    response = await client.delete(f"/api/v1/listings/{listing_id}")

    assert response.status_code == 404

    data = response.json()

    assert data["code"] == "not_found"
    assert str(listing_id) in data["detail"]

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


async def test_listing_get_response_shape(client: AsyncClient, uow: UnitOfWork) -> None:
    listing = await create_listing(uow)

    response = await client.get(
        f"/api/v1/listings/{listing.id}",
    )

    assert response.status_code == 200
    ListingResponse.model_validate(response.json())  # or manual field assertions

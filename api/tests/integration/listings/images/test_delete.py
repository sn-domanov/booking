import uuid

from httpx import AsyncClient

from app.db.uow import UnitOfWork
from tests.helpers.images import image_upload
from tests.helpers.listings import create_listing

# ─────────────────────────────────────────
# DELETE /api/v1/listings/{listing_id}
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 204 No Content
# ─────────────────────────────────────────


async def test_listing_images_delete_success(
    client: AsyncClient,
    uow: UnitOfWork,
    moto_s3,
) -> None:
    listing = await create_listing(uow)

    post_response = await client.post(
        f"/api/v1/listings/{listing.id}/images",
        files=image_upload(),
        data={"position": 1},
    )

    image_id = post_response.json()["id"]

    delete_response = await client.delete(
        f"/api/v1/listings/{listing.id}/images/{image_id}",
    )

    assert delete_response.status_code == 204

    # Database/API state
    get_response = await client.get(
        f"/api/v1/listings/{listing.id}/images",
    )

    data = get_response.json()

    assert len(data) == 0

    # Object storage state
    objects = moto_s3.list_objects_v2(Bucket="booking-test")

    assert objects["KeyCount"] == 0


# ─────────────────────────────────────────
# 404 Not Found
# ─────────────────────────────────────────


async def test_listing_images_delete_not_found(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    listing = await create_listing(uow)

    image_id = uuid.UUID("00000000-0000-0000-0000-000000000000")

    response = await client.delete(
        f"/api/v1/listings/{listing.id}/images/{image_id}",
    )

    assert response.status_code == 404

    data = response.json()

    assert data["code"] == "not_found"
    assert str(image_id) in data["detail"]

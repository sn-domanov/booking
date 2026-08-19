import uuid
from io import BytesIO

from httpx import AsyncClient

from app.db.uow import UnitOfWork
from tests.helpers.images import image_upload
from tests.helpers.listings import create_listing

# ─────────────────────────────────────────
# PATCH /api/v1/listings/{listing_id}/images/{image_id}
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 200 OK
# ─────────────────────────────────────────


async def test_listing_image_update_success(
    client: AsyncClient,
    uow: UnitOfWork,
    moto_s3,
) -> None:
    listing = await create_listing(uow)

    post_response = await client.post(
        f"/api/v1/listings/{listing.id}/images",
        files=image_upload(),
        data={"position": "1"},
    )

    assert post_response.status_code == 201

    image_id = post_response.json()["id"]

    patch_response = await client.patch(
        f"/api/v1/listings/{listing.id}/images/{image_id}",
        data={"position": 2},
    )

    image = patch_response.json()

    assert image["position"] == 2
    assert image["contentType"] == "image/webp"
    assert image["url"].endswith(".webp")

    # Database/API state
    get_response = await client.get(
        f"/api/v1/listings/{listing.id}/images",
    )

    assert get_response.status_code == 200

    images = get_response.json()

    assert len(images) == 1
    assert images[0] == image

    # Object storage state
    objects = moto_s3.list_objects_v2(Bucket="booking-test")

    assert objects["KeyCount"] == 1

    obj = objects["Contents"][0]

    assert image["url"].endswith(obj["Key"])
    assert obj["Size"] > 0


# ─────────────────────────────────────────
# 404 Not Found
# ─────────────────────────────────────────


async def test_listing_image_update_not_found(
    client: AsyncClient,
    uow: UnitOfWork,
):
    listing = await create_listing(uow)

    image_id = uuid.UUID("00000000-0000-0000-0000-000000000000")

    response = await client.patch(
        f"/api/v1/listings/{listing.id}/images/{image_id}",
        data={"position": "1"},
    )

    assert response.status_code == 404

    data = response.json()

    assert data["code"] == "not_found"
    assert str(image_id) in data["detail"]


# ─────────────────────────────────────────
# 422 Application Validation
# ─────────────────────────────────────────


async def test_listing_image_update_invalid_file(
    client: AsyncClient,
    uow: UnitOfWork,
):
    listing = await create_listing(uow)

    post_response = await client.post(
        f"/api/v1/listings/{listing.id}/images",
        files=image_upload(),
        data={"position": "1"},
    )

    assert post_response.status_code == 201

    image_id = post_response.json()["id"]

    patch_response = await client.patch(
        f"/api/v1/listings/{listing.id}/images/{image_id}",
        files={
            "file": (
                "profile.jpg",
                BytesIO(b"Invalid image file"),
                "image/jpeg",
            )
        },
    )

    assert patch_response.status_code == 422

    data = patch_response.json()

    assert data["code"] == "invalid_image"
    assert "invalid" in data["detail"].lower()

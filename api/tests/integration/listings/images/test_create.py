from io import BytesIO

from httpx import AsyncClient

from app.db.uow import UnitOfWork
from tests.helpers.images import image_upload
from tests.helpers.listings import create_listing

# ─────────────────────────────────────────
# POST /api/v1/listings/{listing_id}/images
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 201 Created
# ─────────────────────────────────────────


async def test_listing_image_create_success(
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

    image = post_response.json()

    assert image["position"] == 1
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
# 409 Conflict
# ─────────────────────────────────────────


async def test_create_listing_image_rejects_duplicate_position(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    listing = await create_listing(uow)

    await client.post(
        f"/api/v1/listings/{listing.id}/images",
        files=image_upload(),
        data={"position": "1"},
    )

    response = await client.post(
        f"/api/v1/listings/{listing.id}/images",
        files=image_upload(),
        data={"position": "1"},
    )

    assert response.status_code == 409

    data = response.json()

    assert data["code"] == "conflict"
    assert data["conflict"] == "listing_image_position"
    assert "exists" in data["detail"].lower()
    assert "position" in data["detail"].lower()


# ─────────────────────────────────────────
# 422 Application Validation
# ─────────────────────────────────────────


async def test_listing_image_create_invalid_file(
    client: AsyncClient,
    uow: UnitOfWork,
    moto_s3,
):
    listing = await create_listing(uow)

    response = await client.post(
        f"/api/v1/listings/{listing.id}/images",
        files={
            "file": (
                "profile.jpg",
                BytesIO(b"Invalid image file"),
                "image/jpeg",
            )
        },
        data={"position": 1},
    )
    assert response.status_code == 422

    data = response.json()

    assert data["code"] == "invalid_image"
    assert "invalid" in data["detail"].lower()

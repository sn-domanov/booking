from httpx import AsyncClient

from app.db.uow import UnitOfWork
from tests.helpers.images import image_upload
from tests.helpers.listings import create_listing

# ─────────────────────────────────────────
# GET /api/v1/listings/{listing_id}/images
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 200 OK
# ─────────────────────────────────────────


async def test_listing_images_list_success(
    client: AsyncClient, uow: UnitOfWork
) -> None:
    listing = await create_listing(uow)

    images = [
        (
            await client.post(
                f"/api/v1/listings/{listing.id}/images",
                files=image_upload(),
                data={"position": i},
            )
        ).json()
        for i in range(1, 6)
    ]

    response = await client.get(
        f"/api/v1/listings/{listing.id}/images",
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == len(images)
    assert {item["id"] for item in data} == {str(image["id"]) for image in images}


async def test_listing_images_list_returns_ordered_by_position(
    client: AsyncClient, uow: UnitOfWork
) -> None:
    listing = await create_listing(uow)

    images = [
        (
            await client.post(
                f"/api/v1/listings/{listing.id}/images",
                files=image_upload(),
                data={"position": i},
            )
        ).json()
        for i in range(1, 6)
    ]

    response = await client.get(f"/api/v1/listings/{listing.id}/images")

    assert response.status_code == 200

    data = response.json()

    expected = [
        image["position"] for image in sorted(images, key=lambda img: img["id"])
    ]

    actual = [item["position"] for item in data]

    assert actual == expected

from io import BytesIO
from pathlib import Path

import httpx

from app.domains.listings.api.schemas import ListingResponse

from .data import LISTINGS

IMAGES_DIR = Path(__file__).parent / "assets" / "images"


async def seed_listings(
    client: httpx.AsyncClient,
) -> list[ListingResponse]:
    listings: list[ListingResponse] = []

    for data in LISTINGS:
        # 1. Create listing
        response = await client.post(
            "/api/v1/listings",
            json=data,
        )
        response.raise_for_status()

        listing = ListingResponse.model_validate(response.json())
        listings.append(listing)

        # 2. Create listing images
        for position, image in enumerate(data["images"], start=1):
            path = IMAGES_DIR / image

            response = await client.post(
                f"/api/v1/listings/{listing.id}/images",
                files={
                    "file": (
                        path.name,
                        BytesIO(path.read_bytes()),
                        "image/webp",
                    )
                },
                data={"position": position},
            )
            response.raise_for_status()

    return listings

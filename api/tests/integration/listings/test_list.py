from datetime import UTC, datetime

import pytest
from httpx import AsyncClient

from app.api.schemas import OffsetPageResponse
from app.db.uow import UnitOfWork
from tests.helpers.listings import create_listing

# ─────────────────────────────────────────
# GET /api/v1/listings
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 200 OK
# ─────────────────────────────────────────


async def test_listings_list_empty(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/listings",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []
    assert data["total"] == 0
    assert data["hasNext"] is False


async def test_listings_list_return_created(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    listings = [await create_listing(uow) for _ in range(5)]

    response = await client.get(
        "/api/v1/listings?limit=2&offset=2",
    )

    assert response.status_code == 200

    data = response.json()

    response_ids = {item["id"] for item in data["items"]}
    listing_ids = {str(listing.id) for listing in listings}

    # response_ids <= listing_ids
    assert response_ids.issubset(listing_ids)


async def test_listings_list_returns_newest_first(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    older = await create_listing(
        uow,
        name="Older",
        created_at=datetime(2020, 1, 1, tzinfo=UTC),
    )

    newer = await create_listing(
        uow,
        name="Newer",
        created_at=datetime(2021, 1, 1, tzinfo=UTC),
    )

    response = await client.get(
        "/api/v1/listings",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["items"][0]["id"] == str(newer.id)
    assert data["items"][1]["id"] == str(older.id)

    # Assert server default timestamps were overridden
    assert data["items"][0]["createdAt"] == "2021-01-01T00:00:00Z"
    assert data["items"][1]["createdAt"] == "2020-01-01T00:00:00Z"


async def test_listings_list_uses_id_as_tiebreaker_for_equal_timestamps(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    listings = []

    for i in range(5):
        listings.append(
            await create_listing(
                uow,
                name=f"Listing {i}",
                created_at=datetime(2020, 1, 1, tzinfo=UTC),
            )
        )

    response = await client.get(
        "/api/v1/listings?limit=5&offset=0",
    )

    assert response.status_code == 200

    data = response.json()

    expected = sorted(
        [str(listing.id) for listing in listings],
        reverse=True,
    )

    actual = [item["id"] for item in data["items"]]

    assert actual == expected


@pytest.mark.parametrize(
    "limit,offset,expected_count,has_next",
    [
        (20, 0, 5, False),  # default - all 5
        (2, 0, 2, True),  # first page
        (2, 2, 2, True),  # second page
        (2, 4, 1, False),  # last page
    ],
)
async def test_listings_list_pagination(
    client: AsyncClient,
    uow: UnitOfWork,
    limit,
    offset,
    expected_count,
    has_next,
) -> None:
    [await create_listing(uow) for _ in range(5)]

    response = await client.get(
        f"/api/v1/listings?limit={limit}&offset={offset}",
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == expected_count
    assert data["hasNext"] is has_next
    assert data["total"] == 5


async def test_listings_list_response_shape(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    [await create_listing(uow) for _ in range(5)]

    response = await client.get(
        "/api/v1/listings",
    )

    data = response.json()

    OffsetPageResponse.model_validate(data)  # or manual field assertions

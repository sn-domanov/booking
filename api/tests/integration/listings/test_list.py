from datetime import UTC, datetime

from httpx import AsyncClient

from app.db.uow import UnitOfWork
from tests.helpers.listings import create_listing

# ─────────────────────────────────────────
# GET /api/v1/listings
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 200 OK
# ─────────────────────────────────────────


async def test_listings_list_success(client: AsyncClient, uow: UnitOfWork) -> None:
    listings = [await create_listing(uow) for _ in range(5)]

    response = await client.get("/api/v1/listings")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == len(listings)
    assert {item["id"] for item in data} == {str(listing.id) for listing in listings}


async def test_listings_list_returns_newest_first(
    client: AsyncClient, uow: UnitOfWork
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

    response = await client.get("/api/v1/listings")

    assert response.status_code == 200

    data = response.json()

    assert data[0]["id"] == str(newer.id)
    assert data[1]["id"] == str(older.id)

    # Assert server default timestamps were overridden
    assert data[0]["createdAt"] == "2021-01-01T00:00:00Z"
    assert data[1]["createdAt"] == "2020-01-01T00:00:00Z"


async def test_listings_list_uses_id_as_tiebreaker_for_equal_timestamps(
    client: AsyncClient, uow: UnitOfWork
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

    response = await client.get("/api/v1/listings")

    assert response.status_code == 200

    data = response.json()

    expected = sorted(
        [str(listing.id) for listing in listings],
        reverse=True,
    )

    actual = [item["id"] for item in data]

    assert actual == expected

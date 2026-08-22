from datetime import UTC, datetime

import pytest
from httpx import AsyncClient

from app.api.schemas import CursorPageResponse, OffsetPageResponse
from app.core.pagination import encode_cursor
from app.db.uow import UnitOfWork
from tests.helpers.listings import create_listing

# ─────────────────────────────────────────
# GET /api/v1/listings
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# 200 OK
# ─────────────────────────────────────────


async def test_listings_list_offset_pagination_by_default(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    await create_listing(uow)

    response = await client.get("/api/v1/listings")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "hasNext" in data
    assert "total" in data
    assert "nextCursor" not in data


@pytest.mark.parametrize(
    "pagination",
    ["offset", "cursor"],
)
async def test_listings_list_empty(
    client: AsyncClient,
    pagination: str,
) -> None:
    response = await client.get(
        "/api/v1/listings",
        params={"pagination": pagination},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []

    if pagination == "offset":
        assert data["total"] == 0
        assert data["hasNext"] is False
    else:
        assert data["nextCursor"] is None


@pytest.mark.parametrize(
    "pagination",
    ["offset", "cursor"],
)
async def test_listings_list_return_created(
    client: AsyncClient,
    uow: UnitOfWork,
    pagination: str,
) -> None:
    listings = [await create_listing(uow) for _ in range(5)]

    response = await client.get(
        "/api/v1/listings",
        params={"pagination": pagination},
    )

    assert response.status_code == 200

    data = response.json()

    response_ids = {item["id"] for item in data["items"]}
    listing_ids = {str(listing.id) for listing in listings}

    # response_ids <= listing_ids
    assert response_ids.issubset(listing_ids)


@pytest.mark.parametrize(
    "pagination",
    ["offset", "cursor"],
)
async def test_listings_list_returns_newest_first(
    client: AsyncClient,
    uow: UnitOfWork,
    pagination: str,
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
        params={"pagination": pagination},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["items"][0]["id"] == str(newer.id)
    assert data["items"][1]["id"] == str(older.id)

    # Assert server default timestamps were overridden
    assert data["items"][0]["createdAt"] == "2021-01-01T00:00:00Z"
    assert data["items"][1]["createdAt"] == "2020-01-01T00:00:00Z"


@pytest.mark.parametrize(
    "pagination",
    ["offset", "cursor"],
)
async def test_listings_list_uses_id_as_tiebreaker_for_equal_timestamps(
    client: AsyncClient,
    uow: UnitOfWork,
    pagination: str,
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
        "/api/v1/listings",
        params={"pagination": pagination},
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
    "pagination",
    ["offset", "cursor"],
)
async def test_listings_list_response_shape(
    client: AsyncClient,
    uow: UnitOfWork,
    pagination: str,
) -> None:
    [await create_listing(uow) for _ in range(5)]

    response = await client.get(
        "/api/v1/listings",
        params={"pagination": pagination},
    )

    data = response.json()

    if pagination == "offset":
        OffsetPageResponse.model_validate(data)  # or manual field assertions
    else:
        CursorPageResponse.model_validate(data)


@pytest.mark.parametrize(
    "limit,offset,expected_count,has_next",
    [
        (20, 0, 5, False),  # default - all 5
        (2, 0, 2, True),  # first page
        (2, 2, 2, True),  # second page
        (2, 4, 1, False),  # last page
    ],
)
async def test_listings_list_offset_pagination(
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


async def test_listings_list_cursor_pagination(
    client: AsyncClient,
    uow: UnitOfWork,
) -> None:
    for _ in range(5):
        await create_listing(uow)

    response = await client.get(
        "/api/v1/listings",
        params={
            "pagination": "cursor",
            "limit": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 2
    assert data["nextCursor"] is not None

    first_cursor = data["nextCursor"]

    response = await client.get(
        "/api/v1/listings",
        params={
            "pagination": "cursor",
            "limit": 2,
            "cursor": first_cursor,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 2
    assert data["nextCursor"] is not None

    second_cursor = data["nextCursor"]

    response = await client.get(
        "/api/v1/listings",
        params={
            "pagination": "cursor",
            "limit": 2,
            "cursor": second_cursor,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 1
    assert data["nextCursor"] is None


# ─────────────────────────────────────────
# 422 Request Validation (Pydantic/FastAPI)
# ─────────────────────────────────────────


@pytest.mark.parametrize(
    "params",
    [
        {"limit": 0},
        {"limit": 101},
        {"limit": -1},
        {"offset": -1},
        {"limit": "abc"},
        {"offset": "abc"},
    ],
)
async def test_listings_list_invalid_offset_pagination(
    client: AsyncClient,
    params: dict[str, str | int],
) -> None:
    response = await client.get(
        "/api/v1/listings",
        params=params,
    )

    assert response.status_code == 422


# ─────────────────────────────────────────
# 400 Bad Request
# ─────────────────────────────────────────


async def test_listings_list_cursor_malformed(
    client: AsyncClient,
) -> None:
    response = await client.get(
        "/api/v1/listings",
        params={
            "pagination": "cursor",
            "cursor": "not-a-valid-cursor",
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["code"] == "invalid_cursor"
    assert data["detail"] == "Invalid cursor"


async def test_listings_list_cursor_invalid(
    client: AsyncClient,
) -> None:
    cursor = encode_cursor(
        {
            "created_at": "not-a-date",
            "id": "not-a-uuid",
        }
    )

    response = await client.get(
        "/api/v1/listings",
        params={
            "pagination": "cursor",
            "cursor": cursor,
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["code"] == "invalid_cursor"
    assert data["detail"] == "Invalid cursor"

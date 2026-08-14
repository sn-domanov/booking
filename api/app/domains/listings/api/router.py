from uuid import UUID

from fastapi import APIRouter, status

from app.api.deps.listings import ListingServiceDep
from app.domains.listings.api.schemas import (
    ListingCreate,
    ListingReplace,
    ListingResponse,
    ListingUpdate,
)

router = APIRouter(prefix="/listings", tags=["listings"])


@router.post(
    "",
    response_model=ListingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_listing(
    data: ListingCreate,
    service: ListingServiceDep,
):
    listing = await service.create_listing(data=data)

    return listing


@router.get(
    "",
    response_model=list[ListingResponse],
)
async def list_listings(
    service: ListingServiceDep,
):
    listings = await service.list_listings()

    return listings


@router.get(
    "/{listing_id}",
    response_model=ListingResponse,
)
async def get_listing(
    listing_id: UUID,
    service: ListingServiceDep,
):
    listing = await service.get_listing(listing_id=listing_id)

    return listing


@router.patch(
    "/{listing_id}",
    response_model=ListingResponse,
)
async def update_listing(
    listing_id: UUID,
    data: ListingUpdate,
    service: ListingServiceDep,
):
    listing = await service.update_listing(
        listing_id=listing_id,
        data=data,
    )

    return listing


@router.put(
    "/{listing_id}",
    response_model=ListingResponse,
)
async def replace_listing(
    listing_id: UUID,
    data: ListingReplace,
    service: ListingServiceDep,
):
    listing = await service.replace_listing(
        listing_id=listing_id,
        data=data,
    )

    return listing


@router.delete(
    "/{listing_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_listing(
    listing_id: UUID,
    service: ListingServiceDep,
) -> None:
    await service.delete_listing(listing_id=listing_id)

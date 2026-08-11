from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.deps.listings import ListingServiceDep
from app.domains.listings.api.schemas import (
    ListingCreate,
    ListingReplace,
    ListingResponse,
    ListingUpdate,
)
from app.domains.listings.service import ListingNotFound

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
    listing = await service.create(data=data)

    return listing


@router.get(
    "",
    response_model=list[ListingResponse],
)
async def list_listings(
    service: ListingServiceDep,
):
    listings = await service.list()

    return listings


@router.get(
    "/{listing_id}",
    response_model=ListingResponse,
)
async def get_listing(
    listing_id: UUID,
    service: ListingServiceDep,
):
    try:
        listing = await service.get(listing_id=listing_id)
    except ListingNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

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
    try:
        listing = await service.update(
            listing_id=listing_id,
            data=data,
        )
    except ListingNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

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
    try:
        listing = await service.replace(
            listing_id=listing_id,
            data=data,
        )
    except ListingNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return listing


@router.delete(
    "/{listing_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_listing(
    listing_id: UUID,
    service: ListingServiceDep,
) -> None:
    try:
        await service.delete(listing_id=listing_id)
    except ListingNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.api.deps.listings import ListingServiceDep
from app.api.schemas import OffsetPageResponse, OffsetPaginationQuery
from app.core.pagination import OffsetPage, OffsetPagination
from app.domains.listings.api.images.router import router as images_router
from app.domains.listings.api.schemas import (
    ListingCreate,
    ListingReplace,
    ListingResponse,
    ListingUpdate,
)
from app.domains.listings.dto import ListingResult

router = APIRouter(prefix="/listings", tags=["listings"])


@router.post(
    "",
    response_model=ListingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_listing(
    data: ListingCreate,
    service: ListingServiceDep,
) -> ListingResult:
    listing = await service.create_listing(data=data)

    return listing


@router.get(
    "",
    response_model=OffsetPageResponse[ListingResponse],
)
async def list_listings(
    pagination: Annotated[OffsetPaginationQuery, Query()],
    service: ListingServiceDep,
) -> OffsetPage[ListingResult]:
    return await service.list_listings(
        pagination=OffsetPagination(
            limit=pagination.limit,
            offset=pagination.offset,
        )
    )


@router.get(
    "/{listing_id}",
    response_model=ListingResponse,
)
async def get_listing(
    listing_id: UUID,
    service: ListingServiceDep,
) -> ListingResult:
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
) -> ListingResult:
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
) -> ListingResult:
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


router.include_router(images_router)

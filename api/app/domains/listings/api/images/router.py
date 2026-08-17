from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, File, Form, UploadFile, status

from app.api.deps.listings import ListingServiceDep
from app.domains.listings.api.images.schemas import ListingImageResponse

router = APIRouter(prefix="/{listing_id}/images")


@router.post(
    "", response_model=ListingImageResponse, status_code=status.HTTP_201_CREATED
)
async def create_listing_image(
    listing_id: UUID,
    service: ListingServiceDep,
    file: Annotated[UploadFile, File()],
    position: Annotated[int, Form(gt=0, le=10)],
):
    content = await file.read()

    return await service.add_image(
        listing_id=listing_id,
        image_position=position,
        content=content,
    )


@router.get("", response_model=list[ListingImageResponse])
async def list_listing_images(
    listing_id: UUID,
    service: ListingServiceDep,
):
    return await service.list_images(listing_id=listing_id)


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_listing_image(
    listing_id: UUID,
    image_id: UUID,
    service: ListingServiceDep,
) -> None:
    await service.delete_image(
        listing_id=listing_id,
        image_id=image_id,
    )

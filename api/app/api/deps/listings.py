from typing import Annotated

from fastapi import Depends

from app.api.deps.database import UoWDep
from app.api.deps.media import MediaServiceDep
from app.domains.listings.service import ListingService


def get_listing_service(
    uow: UoWDep,
    media_service: MediaServiceDep,
) -> ListingService:
    return ListingService(uow=uow, media_service=media_service)


ListingServiceDep = Annotated[
    ListingService,
    Depends(get_listing_service),
]

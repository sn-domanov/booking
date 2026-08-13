from typing import Annotated

from fastapi import Depends

from app.api.deps.database import UoWDep
from app.domains.listings.service import ListingService


def get_listing_service(
    uow: UoWDep,
) -> ListingService:
    return ListingService(
        uow=uow,
    )


ListingServiceDep = Annotated[
    ListingService,
    Depends(get_listing_service),
]

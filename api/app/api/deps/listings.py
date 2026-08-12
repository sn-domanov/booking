from typing import Annotated

from fastapi import Depends

from app.api.deps.database import UoWDep
from app.api.deps.settings import SettingsDep
from app.domains.listings.service import ListingService


def get_listing_service(
    settings: SettingsDep,
    uow: UoWDep,
) -> ListingService:
    return ListingService(
        settings=settings,
        uow=uow,
    )


ListingServiceDep = Annotated[
    ListingService,
    Depends(get_listing_service),
]

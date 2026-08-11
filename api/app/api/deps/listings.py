from typing import Annotated

from fastapi import Depends

from app.api.deps.database import SessionDep
from app.api.deps.settings import SettingsDep
from app.domains.listings.repository import ListingRepository
from app.domains.listings.service import ListingService


def get_listing_service(
    settings: SettingsDep,
    session: SessionDep,
) -> ListingService:
    repository = ListingRepository(session)

    return ListingService(
        settings=settings,
        repository=repository,
        session=session,
    )


ListingServiceDep = Annotated[
    ListingService,
    Depends(get_listing_service),
]

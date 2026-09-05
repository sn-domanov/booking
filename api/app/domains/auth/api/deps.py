from typing import Annotated

from fastapi import Depends

from app.api.deps.database import UoWDep
from app.api.deps.settings import SettingsDep
from app.domains.auth.service import AuthService


def get_auth_service(uow: UoWDep, settings: SettingsDep) -> AuthService:
    return AuthService(
        uow=uow,
        settings=settings.auth
    )


AuthServiceDep = Annotated[
    AuthService,
    Depends(get_auth_service),
]

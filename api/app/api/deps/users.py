from typing import Annotated

from fastapi import Depends

from app.api.deps.database import UoWDep
from app.domains.users.service import UserService


def get_user_service(uow: UoWDep) -> UserService:
    return UserService(uow=uow)


UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service),
]

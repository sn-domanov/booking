from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from app.db.uow import UnitOfWork, create_uow


async def get_uow() -> AsyncGenerator[UnitOfWork]:
    async with create_uow() as uow:
        yield uow


UoWDep = Annotated[
    UnitOfWork,
    Depends(get_uow),
]

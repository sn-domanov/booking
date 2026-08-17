from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from app.db.session import session_factory
from app.db.uow import UnitOfWork


async def get_uow() -> AsyncGenerator[UnitOfWork]:
    async with session_factory() as session:
        yield UnitOfWork(session)


UoWDep = Annotated[
    UnitOfWork,
    Depends(get_uow),
]

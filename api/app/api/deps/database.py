from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_factory


async def get_session():
    async with async_session_factory() as session:
        yield session


SessionDep = Annotated[
    AsyncSession,
    Depends(get_session),
]

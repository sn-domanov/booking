from uuid import UUID

from sqlalchemy import select

from app.db.session import AsyncSession
from app.domains.users.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def add(self, *, user: User) -> None:
        self.session.add(user)

    async def get(self, *, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

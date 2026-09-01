from app.db.uow import UnitOfWork
from app.domains.users.models import User
from tests.factories.user import user_factory


async def create_user(uow: UnitOfWork, **overrides) -> User:
    user = user_factory(**overrides)

    async with uow.transaction():
        uow.users.add(user=user)

    return user

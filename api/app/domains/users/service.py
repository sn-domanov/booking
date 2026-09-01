from datetime import UTC, datetime
from uuid import UUID

from app.core.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.core.security import get_password_hash
from app.db.uow import UnitOfWork
from app.domains.users.api.schemas import CurrentUserUpdate, UserCreate
from app.domains.users.models import User


class UserService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_user(self, *, data: UserCreate) -> User:
        async with self.uow.transaction():
            user = self._build_user(data=data)

            self.uow.users.add(user=user)

            return user

    async def create_admin(self, *, data: UserCreate) -> User:
        async with self.uow.transaction():
            user = self._build_user(
                data=data,
                is_admin=True,
            )

            self.uow.users.add(user=user)

            return user

    async def get_user(self, *, user_id: UUID) -> User:
        return await self._get_user(user_id=user_id)

    async def update_current_user(
        self,
        *,
        data: CurrentUserUpdate,
        user: User,
    ) -> User:
        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            raise ValidationError("No fields to update")

        async with self.uow.transaction():
            for field, value in update_data.items():
                setattr(user, field, value)

            return user

    # TODO: move to an use case/application workflow account_deletion
    # when makes service grow grow into a god object
    async def delete_current_user(self, *, user: User) -> None:
        async with self.uow.transaction():
            # TODO: unpublish owner's listings
            user.is_active = False
            user.deleted_at = datetime.now(UTC)

    async def deactivate_user(
        self,
        *,
        user_id: UUID,
        actor: User,
    ) -> None:
        if not actor.is_admin:
            raise ForbiddenError("Admin privileges required")

        async with self.uow.transaction():
            user = await self._get_user(user_id=user_id)
            user.is_active = False

    async def reactivate_user(
        self,
        *,
        user_id: UUID,
        actor: User,
    ) -> None:
        if not actor.is_admin:
            raise ForbiddenError("Admin privileges required")

        async with self.uow.transaction():
            user = await self._get_user(user_id=user_id, include_inactive=True)

            if user.deleted_at is not None:
                raise NotFoundError("User not found")

            user.is_active = True

    async def _get_user(
        self,
        *,
        user_id: UUID,
        include_inactive: bool = False,
    ) -> User:
        user = await self.uow.users.get(user_id=user_id)

        if user is None:
            raise NotFoundError("User not found")

        if not include_inactive and not user.is_active:
            raise NotFoundError("User not found")

        return user

    @staticmethod
    def _build_user(
        *,
        data: UserCreate,
        is_admin: bool = False,
    ) -> User:
        return User(
            email=data.email,
            password_hash=get_password_hash(data.password),
            display_name=data.display_name,
            is_admin=is_admin,
        )

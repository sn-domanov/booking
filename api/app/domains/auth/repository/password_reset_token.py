from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.auth.models import PasswordResetToken


class PasswordResetTokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        *,
        user_id: UUID,
        token_hash: str,
        expires_at: datetime,
    ) -> PasswordResetToken:
        token = PasswordResetToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        self.session.add(token)

        return token

    async def get_by_hash(
        self,
        *,
        token_hash: str,
    ) -> PasswordResetToken | None:
        stmt = select(PasswordResetToken).where(
            PasswordResetToken.token_hash == token_hash,
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_for_user(
        self,
        *,
        user_id: UUID,
    ) -> PasswordResetToken | None:
        stmt = select(PasswordResetToken).where(
            PasswordResetToken.user_id == user_id,
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def delete_for_user(
        self,
        *,
        user_id: UUID,
    ) -> None:
        stmt = delete(PasswordResetToken).where(
            PasswordResetToken.user_id == user_id,
        )

        await self.session.execute(stmt)

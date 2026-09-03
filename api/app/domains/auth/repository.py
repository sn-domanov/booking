from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.auth.models import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_hash_for_update(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        stmt = (
            select(RefreshToken)
            .where(
                RefreshToken.token_hash == token_hash,
            )
            # Lock the row to prevent other transactions from modifying it
            # until the current transaction completes
            .with_for_update()
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        user_id: UUID,
        family_id: UUID,
        token_hash: str,
        expires_at: datetime,
    ) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id,
            family_id=family_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        self.session.add(refresh_token)

        return refresh_token

    async def revoke(
        self,
        refresh_token: RefreshToken,
        *,
        replaced_by_id: UUID | None = None,
    ) -> None:
        # PostgreSQL transaction start time, not wall-clock time
        # to align with other timestamps
        refresh_token.revoked_at = func.now()
        refresh_token.replaced_by_id = replaced_by_id

    async def revoke_family(
        self,
        *,
        family_id: UUID,
    ) -> None:
        stmt = (
            update(RefreshToken)
            .where(
                RefreshToken.family_id == family_id,
                RefreshToken.revoked_at.is_(None),
            )
            .values(revoked_at=func.now())
        )

        await self.session.execute(stmt)

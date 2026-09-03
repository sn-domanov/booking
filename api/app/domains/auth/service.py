from datetime import UTC, datetime
from uuid import uuid7

from app.core.config import JwtSettings
from app.core.exceptions import (
    ExpiredTokenError,
    InvalidCredentialsError,
    InvalidTokenError,
    RefreshTokenReuseError,
)
from app.core.security import hash_refresh_token, verify_password
from app.db.uow import UnitOfWork
from app.domains.auth.dto import LoginResult, TokenPair
from app.domains.auth.tokens import (
    create_access_token,
    create_refresh_token,
)


class AuthService:
    def __init__(
        self,
        uow: UnitOfWork,
        jwt_settings: JwtSettings,
    ) -> None:
        self.uow = uow
        self.jwt_settings = jwt_settings

    async def login(
        self,
        *,
        email: str,
        password: str,
    ) -> LoginResult:
        async with self.uow.transaction():
            now = datetime.now(UTC)

            user = await self.uow.users.get_by_email(email=email)

            if user is None or not verify_password(
                password,
                user.password_hash,
            ):
                raise InvalidCredentialsError("Incorrect email or password")

            access_token = create_access_token(
                user_id=user.id,
                now=now,
                settings=self.jwt_settings,
            )

            refresh_token = create_refresh_token()

            await self.uow.refresh_tokens.create(
                user_id=user.id,
                family_id=uuid7(),
                token_hash=hash_refresh_token(refresh_token),
                expires_at=(now + self.jwt_settings.refresh_token_ttl),
            )

            return LoginResult(
                user=user,
                tokens=TokenPair(
                    access_token=access_token,
                    refresh_token=refresh_token,
                ),
            )

    async def refresh(
        self,
        refresh_token: str,
    ) -> TokenPair:
        async with self.uow.transaction():
            now = datetime.now(UTC)

            refresh_token_record = await self.uow.refresh_tokens.get_by_hash_for_update(
                hash_refresh_token(refresh_token)
            )

            if refresh_token_record is None:
                raise InvalidTokenError("Invalid refresh token")

            if refresh_token_record.revoked_at is not None:
                await self.uow.refresh_tokens.revoke_family(
                    family_id=refresh_token_record.family_id
                )
                raise RefreshTokenReuseError("Authentication failed")

            if refresh_token_record.expires_at <= now:
                raise ExpiredTokenError("Refresh token has expired")

            user = await self.uow.users.get(user_id=refresh_token_record.user_id)

            if user is None:
                raise InvalidTokenError("Invalid refresh token")

            new_refresh_token = create_refresh_token()

            new_refresh_token_record = await self.uow.refresh_tokens.create(
                user_id=user.id,
                family_id=refresh_token_record.family_id,
                token_hash=hash_refresh_token(new_refresh_token),
                expires_at=now + self.jwt_settings.refresh_token_ttl,
            )
            # TODO: experiment with when the feature is ready
            await self.uow.session.flush()

            await self.uow.refresh_tokens.revoke(
                refresh_token_record,
                replaced_by_id=new_refresh_token_record.id,
            )

            access_token = create_access_token(
                user_id=user.id,
                now=now,
                settings=self.jwt_settings,
            )

            return TokenPair(
                access_token=access_token,
                refresh_token=new_refresh_token,
            )

    async def logout(self, *, refresh_token: str | None) -> None:
        async with self.uow.transaction():
            if refresh_token is None:
                return

            refresh_token_record = await self.uow.refresh_tokens.get_by_hash_for_update(
                token_hash=hash_refresh_token(refresh_token)
            )

            if refresh_token_record is None:
                return

            if refresh_token_record.revoked_at is None:
                await self.uow.refresh_tokens.revoke(
                    refresh_token_record,
                )

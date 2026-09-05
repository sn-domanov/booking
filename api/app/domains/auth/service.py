from datetime import UTC, datetime
from uuid import uuid7

from app.core.config import AuthSetting
from app.core.exceptions import (
    ExpiredRefreshTokenError,
    InvalidCredentialsError,
    InvalidPasswordResetTokenError,
    InvalidRefreshTokenError,
    RefreshTokenReuseError,
)
from app.core.security import (
    hash_password,
    hash_token,
    verify_password,
)
from app.db.uow import UnitOfWork
from app.domains.auth.dto import LoginResult, PasswordResetFlow, TokenPair
from app.domains.auth.tokens import (
    create_access_token,
    create_password_reset_token,
    create_refresh_token,
)


class AuthService:
    def __init__(
        self,
        uow: UnitOfWork,
        settings: AuthSetting,
    ) -> None:
        self.uow = uow
        self.settings = settings

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
                settings=self.settings.jwt,
            )

            refresh_token = create_refresh_token()

            await self.uow.refresh_tokens.create(
                user_id=user.id,
                family_id=uuid7(),
                token_hash=hash_token(refresh_token),
                expires_at=(now + self.settings.jwt.refresh_token_ttl),
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
                hash_token(refresh_token)
            )

            if refresh_token_record is None:
                raise InvalidRefreshTokenError("Invalid refresh token")

            if refresh_token_record.revoked_at is not None:
                await self.uow.refresh_tokens.revoke_family(
                    family_id=refresh_token_record.family_id
                )
                raise RefreshTokenReuseError("Authentication failed")

            if refresh_token_record.expires_at <= now:
                raise ExpiredRefreshTokenError("Refresh token has expired")

            user = await self.uow.users.get(user_id=refresh_token_record.user_id)

            if user is None:
                raise InvalidRefreshTokenError("Invalid refresh token")

            new_refresh_token = create_refresh_token()

            new_refresh_token_record = await self.uow.refresh_tokens.create(
                user_id=user.id,
                family_id=refresh_token_record.family_id,
                token_hash=hash_token(new_refresh_token),
                expires_at=now + self.settings.jwt.refresh_token_ttl,
            )

            await self.uow.session.flush()

            await self.uow.refresh_tokens.revoke(
                refresh_token_record,
                replaced_by_id=new_refresh_token_record.id,
            )

            access_token = create_access_token(
                user_id=user.id,
                now=now,
                settings=self.settings.jwt,
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
                token_hash=hash_token(refresh_token)
            )

            if refresh_token_record is None:
                return

            if refresh_token_record.revoked_at is None:
                await self.uow.refresh_tokens.revoke(
                    refresh_token_record,
                )

    async def create_password_reset_flow(
        self,
        *,
        email: str,
    ) -> PasswordResetFlow | None:
        async with self.uow.transaction():
            now = datetime.now(UTC)
            user = await self.uow.users.get_by_email(email=email)

            if user is None or not user.is_active:
                return None

            await self.uow.password_reset_tokens.delete_for_user(
                user_id=user.id,
            )

            token = create_password_reset_token()

            await self.uow.password_reset_tokens.create(
                user_id=user.id,
                token_hash=hash_token(token),
                expires_at=now + self.settings.password_reset_token_ttl,
            )

            return PasswordResetFlow(
                token=token,
                email=user.email,
                display_name=user.display_name,
            )

    async def reset_password(
        self,
        *,
        token: str,
        new_password: str,
    ) -> None:
        async with self.uow.transaction():
            now = datetime.now(UTC)
            token_hash = hash_token(token)

            token_record = await self.uow.password_reset_tokens.get_by_hash(
                token_hash=token_hash,
            )

            if token_record is None or token_record.expires_at <= now:
                raise InvalidPasswordResetTokenError(
                    "Invalid or expired token",
                )

            user = await self.uow.users.get(user_id=token_record.user_id)

            if user is None or not user.is_active:
                raise InvalidPasswordResetTokenError(
                    "Invalid or expired token",
                )

            user.password_hash = hash_password(new_password)

            await self.uow.password_reset_tokens.delete_for_user(
                user_id=user.id,
            )

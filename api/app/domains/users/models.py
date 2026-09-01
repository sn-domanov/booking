from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid7

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.domains.listings.models import Listing


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid7,
    )

    email: Mapped[str] = mapped_column(
        String(254),
        unique=True,
        nullable=False,
    )
    display_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
    is_admin: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    listings: Mapped[list[Listing]] = relationship(
        back_populates="owner",
    )
    deleted_at: Mapped[datetime | None]

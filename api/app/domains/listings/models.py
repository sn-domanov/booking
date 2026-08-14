from decimal import Decimal
from uuid import UUID, uuid7

from sqlalchemy import CheckConstraint, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin


class Listing(TimestampMixin, Base):
    __tablename__ = "listings"
    __table_args__ = (
        CheckConstraint(
            "price_per_night > 0",
            name="positive_price",
        ),
        CheckConstraint(
            "max_guests > 0",
            name="positive_max_guests",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid7,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    price_per_night: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
        nullable=False,
    )
    max_guests: Mapped[int] = mapped_column(nullable=False)

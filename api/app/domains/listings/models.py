from decimal import Decimal
from uuid import UUID, uuid7

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    images: Mapped[list[ListingImage]] = relationship(
        back_populates="listing",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ListingImage(TimestampMixin, Base):
    __tablename__ = "listing_images"
    __table_args__ = (
        UniqueConstraint(
            "listing_id",
            "position",
            name="uq_listing_image_position",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid7,
    )
    listing_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("listings.id", ondelete="CASCADE"),
        nullable=False,
    )
    storage_key: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )

    # MIME media type
    content_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    position: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
    )

    listing: Mapped[Listing] = relationship(
        back_populates="images",
    )

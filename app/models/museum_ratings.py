from sqlalchemy import Integer, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MuseumRating(Base):
    __tablename__ = "museum_ratings"

    id: Mapped[int] = mapped_column(primary_key=True)

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    museum_id: Mapped[int] = mapped_column(
        ForeignKey("museums.id", ondelete="CASCADE"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("user_id", "museum_id"),
        CheckConstraint("rating BETWEEN 1 AND 5"),
    )

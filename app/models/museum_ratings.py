from sqlalchemy import Integer, ForeignKey, UniqueConstraint, CheckConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MuseumRating(Base):
    __tablename__ = "museum_ratings"

    id: Mapped[int] = mapped_column(primary_key=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    museum_id: Mapped[int] = mapped_column(ForeignKey("museums.id", ondelete="CASCADE"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="ratings")

    museum: Mapped["Museum"] = relationship("Museum", back_populates="ratings")

    __table_args__ = (
        UniqueConstraint("user_id", "museum_id"),
        CheckConstraint("rating BETWEEN 1 AND 5"),
    )

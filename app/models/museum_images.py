from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MuseumImage(Base):
    __tablename__ = "museum_images"

    __table_args__ = (
        UniqueConstraint(
            "museum_id",
            "position",
            name="uq_museum_image_position"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    image_url: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    position: Mapped[int] = mapped_column(
        nullable=False
    )

    museum_id: Mapped[int] = mapped_column(
        ForeignKey("museums.id", ondelete="CASCADE"),
        nullable=False
    )

    museum: Mapped["Museum"] = relationship(
        back_populates="images"
    )

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Exhibit(Base):
    __tablename__ = "exhibits"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    museum_id: Mapped[int] = mapped_column(
        ForeignKey("museums.id", ondelete="CASCADE"),
        nullable=False,
    )

    museum: Mapped["Museum"] = relationship(
        "Museum",
        back_populates="exhibits",
    )

    images: Mapped[list["ExhibitImage"]] = relationship(
        back_populates="exhibit",
        cascade="all, delete-orphan",
        order_by="ExhibitImage.position"
    )

    models: Mapped[list["ExhibitModel"]] = relationship(
        back_populates="exhibit",
        cascade="all, delete-orphan",
        order_by="ExhibitModel.position"
    )

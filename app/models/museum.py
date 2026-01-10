from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Museum(Base):
    __tablename__ = "museums"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))

    audios: Mapped[list["MuseumAudio"]] = relationship(
        back_populates="museum",
        cascade="all, delete-orphan",
        order_by="MuseumAudio.position",
    )

    images: Mapped[list["MuseumImage"]] = relationship(
        back_populates="museum",
        cascade="all, delete-orphan",
        order_by="MuseumImage.position"
    )

    exhibits: Mapped[list["Exhibit"]] = relationship(
        back_populates="museum",
        cascade="all, delete-orphan",
    )

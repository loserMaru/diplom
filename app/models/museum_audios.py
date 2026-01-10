from sqlalchemy import String, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MuseumAudio(Base):
    __tablename__ = "museum_audios"

    id: Mapped[int] = mapped_column(primary_key=True)
    audio_url: Mapped[str] = mapped_column(String(512), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    museum_id: Mapped[int] = mapped_column(
        ForeignKey("museums.id", ondelete="CASCADE"),
        nullable=False,
    )

    museum: Mapped["Museum"] = relationship(
        "Museum",
        back_populates="audios",
    )

    __table_args__ = (
        UniqueConstraint("museum_id", "position"),
    )

from sqlalchemy import String, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ExhibitImage(Base):
    __tablename__ = "exhibit_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(512), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    exhibit_id: Mapped[int] = mapped_column(
        ForeignKey("exhibits.id", ondelete="CASCADE"),
        nullable=False,
    )

    exhibit: Mapped["Exhibit"] = relationship(
        "Exhibit",
        back_populates="images",
    )

    __table_args__ = (
        UniqueConstraint("exhibit_id", "position"),
    )

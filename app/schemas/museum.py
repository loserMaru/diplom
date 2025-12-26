from pydantic import BaseModel

from app.schemas.museum_images import MuseumImageForMuseum
from app.schemas.shared import ExhibitForMuseum


class MuseumBase(BaseModel):
    name: str
    description: str


class MuseumCreate(MuseumBase):
    pass


class MuseumUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class MuseumPublic(MuseumBase):
    id: int
    images: list[MuseumImageForMuseum]
    exhibits: list[ExhibitForMuseum]

    class Config:
        from_attributes = True

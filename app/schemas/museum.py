from pydantic import BaseModel

from app.schemas.exhibit import ExhibitPublic
from app.schemas.museum_images import MuseumImagePublic


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
    images: list[MuseumImagePublic]
    exhibits: list[ExhibitPublic]

    class Config:
        from_attributes = True

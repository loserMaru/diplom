from pydantic import BaseModel

from app.schemas.exhibit_image import ExhibitImagePublic


class MuseumForExhibits(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class ExhibitForMuseum(BaseModel):
    id: int
    name: str
    description: str
    images: list[ExhibitImagePublic]

    class Config:
        from_attributes = True

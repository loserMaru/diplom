from pydantic import BaseModel

from app.schemas.exhibit_image import ExhibitImagePublic


class ExhibitBase(BaseModel):
    name: str
    description: str


class ExhibitCreate(ExhibitBase):
    museum_id: int


class ExhibitUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ExhibitPublic(ExhibitBase):
    id: int
    images: list[ExhibitImagePublic]

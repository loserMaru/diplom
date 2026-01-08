from pydantic import BaseModel

from app.schemas.exhibit_image import ExhibitImagePublic
from app.schemas.exhibit_models import ExhibitModelPublic
from app.schemas.shared import MuseumForExhibits


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
    museum: MuseumForExhibits
    images: list[ExhibitImagePublic]
    models: list[ExhibitModelPublic]

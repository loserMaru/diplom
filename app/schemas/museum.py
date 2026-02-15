from typing import List

from pydantic import BaseModel

from app.schemas.museum_audios import MuseumAudioForMuseum
from app.schemas.museum_images import MuseumImageForMuseum
from app.schemas.museum_ratings import MuseumRatingPublic
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
    audios: list[MuseumAudioForMuseum]
    images: list[MuseumImageForMuseum]
    exhibits: list[ExhibitForMuseum]

    rating_avg: float
    rating_count: int
    rating_distribution: dict[int, int]

    class Config:
        from_attributes = True


class MuseumSinglePublic(BaseModel):
    id: int
    name: str
    description: str
    audios: List[MuseumAudioForMuseum]
    images: List[MuseumImageForMuseum]
    exhibits: List[ExhibitForMuseum]

    rating_avg: float
    rating_count: int
    rating_distribution: dict[int, int]

    ratings: List[MuseumRatingPublic]  # вот отдельная секция с комментариями

    class Config:
        from_attributes = True
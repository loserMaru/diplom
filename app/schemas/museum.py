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

    class Config:
        from_attributes = True


class MuseumWithStats(MuseumPublic):
    rating_avg: float
    rating_count: int
    rating_distribution: dict[int, int]


class MuseumSinglePublic(MuseumPublic):
    rating_avg: float
    rating_count: int
    rating_distribution: dict[int, int]

    ratings: list[MuseumRatingPublic]

    class Config:
        from_attributes = True

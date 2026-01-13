from pydantic import BaseModel


class MuseumRatingBase(BaseModel):
    rating: int
    museum_id: int


class MuseumRatingCreate(MuseumRatingBase):
    pass


class MuseumRatingUpdate(BaseModel):
    rating: int | None = None
    museum_id: int | None = None


class MuseumRatingPublic(MuseumRatingBase):
    id: int

    class Config:
        from_attributes = True

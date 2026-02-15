from pydantic import BaseModel


class MuseumRatingBase(BaseModel):
    rating: int
    comment: str
    museum_id: int


class MuseumRatingCreate(MuseumRatingBase):
    pass


class MuseumRatingUpdate(BaseModel):
    rating: int | None = None
    comment: str | None = None
    museum_id: int | None = None


class MuseumRatingPublic(MuseumRatingBase):
    id: int
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

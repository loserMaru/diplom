from pydantic import BaseModel


class MuseumImageBase(BaseModel):
    image_url: str
    position: int
    museum_id: int


class MuseumImageCreate(MuseumImageBase):
    pass


class MuseumImageUpdate(BaseModel):
    image_url: str | None = None
    position: int | None = None
    museum_id: int


class MuseumImagePublic(MuseumImageBase):
    id: int

    class Config:
        from_attributes = True
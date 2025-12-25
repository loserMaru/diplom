from pydantic import BaseModel


class ExhibitImageBase(BaseModel):
    image_url: str
    position: str
    exhibit_id: int


class ExhibitImageCreate(ExhibitImageBase):
    pass


class ExhibitImageUpdate(BaseModel):
    image_url: str | None = None
    position: str | None = None
    exhibit_id: int | None = None


class ExhibitImagePublic(ExhibitImageBase):
    id: int

    class Config:
        from_attributes = True
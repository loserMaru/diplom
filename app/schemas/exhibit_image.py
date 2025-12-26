from pydantic import BaseModel


class ExhibitImageBase(BaseModel):
    image_url: str
    position: int
    exhibit_id: int


class ExhibitImageCreate(ExhibitImageBase):
    pass


class ExhibitImageUpdate(BaseModel):
    image_url: str | None = None
    position: int | None = None
    exhibit_id: int | None = None


class ExhibitImagePublic(ExhibitImageBase):
    id: int

    class Config:
        from_attributes = True


class ExhibitImageForExhibit(BaseModel):
    id: int
    image_url: str
    position: int

    class Config:
        from_attributes = True
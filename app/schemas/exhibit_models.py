from pydantic import BaseModel


class ExhibitModelBase(BaseModel):
    model_url: str
    position: int
    exhibit_id: int


class ExhibitModelCreate(ExhibitModelBase):
    pass


class ExhibitModelUpdate(BaseModel):
    model_url: str | None = None
    position: int | None = None
    exhibit_id: int | None = None


class ExhibitModelPublic(ExhibitModelBase):
    id: int

    class Config:
        from_attributes = True


class ExhibitModelForExhibit(BaseModel):
    id: int
    model_url: str
    position: int

    class Config:
        from_attributes = True

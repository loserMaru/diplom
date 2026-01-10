from pydantic import BaseModel


class MuseumAudioBase(BaseModel):
    audio_url: str
    title: str
    position: int
    museum_id: int


class MuseumAudioCreate(MuseumAudioBase):
    pass


class MuseumAudioUpdate(BaseModel):
    audio_url: str | None = None
    title: str | None = None
    position: int | None = None
    museum_id: int | None = None


class MuseumAudioPublic(MuseumAudioBase):
    id: int
    duration: int

    class Config:
        from_attributes = True


class MuseumAudioForMuseum(BaseModel):
    id: int
    audio_url: str
    title: str
    duration: int
    position: int

    class Config:
        from_attributes = True

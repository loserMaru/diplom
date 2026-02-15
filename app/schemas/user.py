from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from pydantic import BaseModel, EmailStr, field_serializer


class UserBase(BaseModel):
    email: EmailStr
    role: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = None


class UserPublic(UserBase):
    id: int
    registered_at: datetime

    @field_serializer("registered_at")
    def serialize(self, value: datetime) -> str:
        moscow = ZoneInfo("Europe/Moscow")

        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        return value.astimezone(moscow).strftime("%d.%m.%Y %H:%M:%S")

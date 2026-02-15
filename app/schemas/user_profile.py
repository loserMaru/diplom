from pydantic import BaseModel

class UserProfileBase(BaseModel):
    first_name: str
    last_name: str


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass


class UserProfilePublic(UserProfileBase):
    id: int

from pydantic import BaseModel


class ProfileCreate(BaseModel):
    bio: str
    user_id: int


class ProfileUpdate(BaseModel):
    bio: str


class ProfileResponse(ProfileCreate):
    id: int

    class Config:
        from_attributes = True

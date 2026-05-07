from pydantic import BaseModel, ConfigDict


class ProfileCreate(BaseModel):
    bio: str
    user_id: int


class ProfileUpdate(BaseModel):
    bio: str


class ProfileResponse(ProfileCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

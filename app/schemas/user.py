from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    age: int


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

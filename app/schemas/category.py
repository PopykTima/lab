from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str


class CategoryResponse(CategoryCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

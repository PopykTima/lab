from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    title: str
    price: int
    category_id: int


class ProductUpdate(ProductCreate):
    pass


class ProductResponse(ProductCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

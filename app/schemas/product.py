from pydantic import BaseModel


class ProductCreate(BaseModel):
    title: str
    price: int
    category_id: int


class ProductUpdate(ProductCreate):
    pass


class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True

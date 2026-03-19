from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

class UserResponse(UserCreate):
    id: int
    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(CategoryCreate):
    id: int
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    title: str
    price: int
    category_id: int

class ProductResponse(ProductCreate):
    id: int
    class Config:
        from_attributes = True
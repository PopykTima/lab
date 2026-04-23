from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

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
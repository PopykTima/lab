from pydantic import BaseModel

# === СХЕМИ ДЛЯ ЮЗЕРІВ (Змінено для Лаби 5) ===

class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    password: str  # Додали обов'язкове поле для пароля при реєстрації

class UserResponse(BaseModel):
    # Тут ми явно прописуємо поля, і НЕ вказуємо password, щоб він не витік!
    id: int
    name: str
    email: str
    age: int
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    # Окрема схема спеціально для форми входу
    email: str
    password: str


# === СХЕМИ ДЛЯ КАТЕГОРІЙ (Залишилися як були) ===

class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(CategoryCreate):
    id: int
    class Config:
        from_attributes = True


# === СХЕМИ ДЛЯ ТОВАРІВ (Залишилися як були) ===

class ProductCreate(BaseModel):
    title: str
    price: int
    category_id: int

class ProductResponse(ProductCreate):
    id: int
    class Config:
        from_attributes = True
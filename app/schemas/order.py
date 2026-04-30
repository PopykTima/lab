from pydantic import BaseModel


class OrderCreate(BaseModel):
    item_name: str
    user_id: int


class OrderUpdate(OrderCreate):
    pass


class OrderResponse(OrderCreate):
    id: int

    class Config:
        from_attributes = True

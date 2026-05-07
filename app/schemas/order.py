from pydantic import BaseModel, ConfigDict


class OrderCreate(BaseModel):
    item_name: str
    user_id: int


class OrderUpdate(OrderCreate):
    pass


class OrderResponse(OrderCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

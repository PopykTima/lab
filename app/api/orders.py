from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.database import get_db
from app.metrics import orders_created_counter
from app.schemas import OrderCreate, OrderResponse, OrderUpdate

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse)
async def create_order(order_in: OrderCreate, db: AsyncSession = Depends(get_db)):
    order = await crud.create_order(db, order_in)
    if order is None:
        raise HTTPException(status_code=404, detail="User not found")
    orders_created_counter.inc()
    return order


@router.get("/", response_model=list[OrderResponse])
async def read_orders(db: AsyncSession = Depends(get_db)):
    return await crud.get_orders(db)


@router.get("/{order_id}", response_model=OrderResponse)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await crud.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(order_id: int, order_in: OrderUpdate, db: AsyncSession = Depends(get_db)):
    order = await crud.update_order(db, order_id, order_in)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{order_id}")
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_order(db, order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted"}

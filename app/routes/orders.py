from fastapi import APIRouter, HTTPException
from app.controllers.orders_controller import list_orders, get_order

router = APIRouter()


@router.get("/orders")
def get_orders(page: int = 1, size: int = 10):
    return list_orders(page, size)


@router.get("/orders/{order_id}")
def get_single_order(order_id: str):
    order = get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="order not found")
    return order

from fastapi import APIRouter
from pydantic import BaseModel
from app.controllers.checkout_controller import checkout

router = APIRouter()


class CheckoutRequest(BaseModel):
    cart_total: float
    coupons: list[str] = []


@router.post("/checkout")
def post_checkout(body: CheckoutRequest):
    return checkout(body.cart_total, body.coupons)

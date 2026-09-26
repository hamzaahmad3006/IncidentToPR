from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.controllers.quotes_controller import create_quote

router = APIRouter()


class QuoteLine(BaseModel):
    sku: str
    price: float = Field(gt=0)
    qty: int = Field(ge=1)


class QuoteRequest(BaseModel):
    lines: list[QuoteLine]
    discount_percent: float = Field(default=0, ge=0, le=100)


@router.post("/quotes")
def post_quote(body: QuoteRequest):
    lines = [{"price": line.price, "qty": line.qty} for line in body.lines]
    return create_quote(lines, body.discount_percent)

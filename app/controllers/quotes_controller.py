from decimal import Decimal, ROUND_HALF_UP


def line_total(price: float, qty: int) -> Decimal:
    return Decimal(str(price)) * qty


def quote_total(lines: list[dict], discount_percent: float) -> float:
    total = sum(line_total(line["price"], line["qty"]) for line in lines)
    factor = (100 - Decimal(str(discount_percent))) / 100
    result = (total * factor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(result)


def create_quote(lines: list[dict], discount_percent: float) -> dict:
    return {"total": quote_total(lines, discount_percent), "currency": "USD"}

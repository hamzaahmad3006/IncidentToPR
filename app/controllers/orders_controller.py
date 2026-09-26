from math import ceil
from app.data import ORDERS


def paginate(items: list, page: int, size: int) -> dict:
    start = (page - 1) * size
    end = start + size
    total_pages = ceil(len(items) / size)
    return {"page": page, "size": size, "total_pages": total_pages, "items": items[start:end]}


def list_orders(page: int, size: int) -> dict:
    return paginate(ORDERS, page, size)


def get_order(order_id: str) -> dict | None:
    for order in ORDERS:
        if order["id"] == order_id:
            return order
    return None

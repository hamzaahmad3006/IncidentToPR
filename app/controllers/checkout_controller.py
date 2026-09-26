from app.data import COUPONS


def resolve_coupons(codes: list[str], applied: list[str] | None = None) -> list[str]:
    applied = [] if applied is None else applied
    for code in codes:
        if code in COUPONS and code not in applied:
            applied.append(code)
    return applied


def discount_for(codes: list[str]) -> int:
    return sum(COUPONS[c] for c in resolve_coupons(codes))


def checkout(cart_total: float, coupons: list[str]) -> dict:
    pct = discount_for(coupons)
    return {"discount_percent": pct, "payable": round(cart_total * (100 - pct) / 100, 2)}

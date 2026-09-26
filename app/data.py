ORDERS = [
    {"id": f"ORD-{i:04d}", "customer": f"customer-{(i % 7) + 1}", "amount": round(10 + i * 3.5, 2)}
    for i in range(1, 26)
]

COUPONS = {"WELCOME10": 10, "SPRING5": 5}

from fastapi import FastAPI
from app.routes import orders_router, quotes_router, checkout_router

app = FastAPI(title="ShopLite API")

app.include_router(orders_router)
app.include_router(quotes_router)
app.include_router(checkout_router)

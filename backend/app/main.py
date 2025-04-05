from fastapi import FastAPI

from app.logging_config import setup_logging
from app.orders.router import router as router_orders

setup_logging()

app = FastAPI(
    title="Logistics API",
    description="API для управления заказами, машинами и путевыми листами",
    version="1.0.0",
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Добро пожаловать в Logistics API 🚚"}


app.include_router(router_orders)

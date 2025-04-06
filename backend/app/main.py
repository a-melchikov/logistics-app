from fastapi import FastAPI

from app.logging_config import setup_logging
from app.orders.router import router as router_orders

setup_logging()

app = FastAPI(
    title="🚚 Logistics API",
    description="API для управления заказами, машинами и путевыми листами",
    version="1.0.0",
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


@app.get("/", tags=["Главная страница"], summary="Приветствие")
def root() -> dict[str, str]:
    """
    Простой приветственный маршрут, чтобы проверить, что API работает.
    """
    return {"message": "Добро пожаловать в Logistics API 🚚"}


app.include_router(router_orders)

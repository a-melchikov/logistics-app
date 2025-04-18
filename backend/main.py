import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.logging_config import setup_logging
from app.orders.router import router as router_orders
from app.trip_sheets.router import router as router_trip_sheets
from app.users.router import router as router_users
from app.vehicles.router import router as router_vehicles

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Главная страница"], summary="Приветствие")
def root() -> dict[str, str]:
    """
    Простой приветственный маршрут, чтобы проверить, что API работает.
    """
    return {"message": "Добро пожаловать в Logistics API 🚚"}


app.include_router(router_users)
app.include_router(router_orders)
app.include_router(router_vehicles)
app.include_router(router_trip_sheets)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

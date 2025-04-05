import logging

from fastapi import APIRouter, Depends

from app.orders.dao import OrderDAO
from app.orders.rb import RBOrder
from app.orders.schemas import OrderResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/orders", tags=["Заказы"])


@router.get("/", summary="Получить все заказы")
async def get_all_orders(request_body: RBOrder = Depends()) -> list[OrderResponse]:
    logger.info(f"Запрос на получение заказов с параметрами: {request_body.to_dict()}")
    orders = await OrderDAO.find_all(**request_body.to_dict())
    logger.info(f"Найдено заказов: {len(orders)}")
    return orders

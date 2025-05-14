import logging

from fastapi import APIRouter, Body, Depends, Path, Response, status

from app.exceptions import OrderNotFoundException, UserNotFoundException
from app.orders.dao import OrderDAO
from app.orders.rb import RBOrder
from app.orders.schemas import OrderCreate, OrderResponse
from app.users.dao import UserDAO
from app.users.dependencies import get_current_admin_user
from app.users.models import User

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/orders",
    tags=["Заказы"],
)


@router.get(
    "/",
    response_model=list[OrderResponse],
    summary="Получить все заказы",
    description="Возвращает список всех заказов, с возможностью фильтрации по параметрам.",
)
async def get_all_orders(request_body: RBOrder = Depends()) -> list[OrderResponse]:
    logger.info(f"Запрос на получение заказов с параметрами: {request_body.to_dict()}")
    orders = await OrderDAO.find_all_filtered(**request_body.to_dict())
    logger.info(f"Найдено заказов: {len(orders)}")
    return orders


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Получить заказ по ID",
    description="Возвращает заказ по его уникальному идентификатору.",
    responses={404: {"description": "Заказ не найден"}},
)
async def get_one_order_by_id(
    order_id: int = Path(..., description="ID заказа, который нужно получить"),
) -> OrderResponse:
    order = await OrderDAO.find_one_or_none_by_id(order_id)
    if not order:
        logger.warning(f"Заказ с ID {order_id} не найден")
        raise OrderNotFoundException
    logger.info(f"Получен заказ с ID {order_id}")
    return order


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать заказ",
    description="Создаёт новый заказ. Проверяет наличие пользователя по `created_by_id`.",
    responses={404: {"description": "Заказ не найден"}},
)
async def create_order(
    order_data: OrderCreate = Body(
        ..., description="Данные для создания нового заказа"
    ),
    _: User = Depends(get_current_admin_user),
) -> OrderResponse:
    logger.info(f"Создание заказа: {order_data}")
    user = await UserDAO.find_one_or_none_by_id(order_data.created_by_id)
    if user is None:
        logger.warning(f"Пользователь с ID {order_data.created_by_id} не найден")
        raise UserNotFoundException
    created_order = await OrderDAO.add(**order_data.model_dump())
    logger.info(f"Создан заказ с ID {created_order.id}")
    return created_order


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить заказ по ID",
    description="Удаляет заказ по ID. Возвращает статус 204, если удаление прошло успешно.",
    responses={404: {"description": "Заказ не найден"}},
)
async def delete_order(
    order_id: int = Path(..., description="ID заказа, который нужно удалить"),
    _: User = Depends(get_current_admin_user),
) -> Response:
    logger.info(f"Попытка удалить заказ с ID {order_id}")
    deleted_count = await OrderDAO.delete(id=order_id)
    if deleted_count == 0:
        logger.warning(f"Заказ с ID {order_id} не найден для удаления")
        raise OrderNotFoundException
    logger.info(f"Удалён заказ с ID {order_id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

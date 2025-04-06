import logging

from fastapi import APIRouter, Body, Depends, Path, Response, status

from app.exceptions import VehicleNotFoundException
from app.orders.schemas import OrderResponse
from app.vehicles.dao import VehicleDAO
from app.vehicles.rb import RBVehicle
from app.vehicles.schemas import VehicleCreate, VehicleResponse

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/vehicles",
    tags=["Машины"],
)


@router.get(
    "/",
    response_model=list[VehicleResponse],
    summary="Получить все машины",
    description="Возвращает список всех машин с возможностью фильтрации.",
)
async def get_all_vehicles(
    request_body: RBVehicle = Depends(),
) -> list[VehicleResponse]:
    logger.info("Запрос на получение всех машин")
    vehicles = await VehicleDAO.find_all(**request_body.to_dict())
    logger.info(f"Найдено машин: {len(vehicles)}")
    return vehicles


@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse,
    summary="Получить машину по ID",
    description="Возвращает информацию о машине по его уникальному идентификатору.",
    responses={404: {"description": "Машина не найдена"}},
)
async def get_one_vehicle_by_id(
    vehicle_id: int = Path(..., description="ID машины, которую нужно получить"),
) -> VehicleResponse:
    vehicle = await VehicleDAO.find_one_or_none_by_id(vehicle_id)
    if not vehicle:
        logger.warning(f"Машина с ID {vehicle_id} не найдена")
        raise VehicleNotFoundException
    logger.info(f"Получена информация о машине с ID {vehicle_id}")
    return vehicle


@router.post(
    "/",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать машину",
    description="Создаёт новый автомобиль.",
)
async def create_vehicle(
    vehicle_data: VehicleCreate = Body(
        ..., description="Данные для создания нового автомобиля"
    ),
) -> VehicleResponse:
    logger.info(f"Создание машины: {vehicle_data}")
    created_vehicle = await VehicleDAO.add(**vehicle_data.model_dump())
    logger.info(f"Создана машина с ID {created_vehicle.id}")
    return created_vehicle


@router.delete(
    "/{vehicle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить машину",
    description="Удаляет машину по ID. Возвращает статус 204, если удаление прошло успешно.",
    responses={404: {"description": "Машина не найдена"}},
)
async def delete_vehicle(
    vehicle_id: int = Path(..., description="ID машины, которую нужно удалить"),
) -> Response:
    logger.info(f"Попытка удалить машину с ID {vehicle_id}")
    deleted_count = await VehicleDAO.delete(id=vehicle_id)
    if deleted_count == 0:
        logger.warning(f"Машина с ID {vehicle_id} не найдена для удаления")
        raise VehicleNotFoundException
    logger.info(f"Удалена машина с ID {vehicle_id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{vehicle_id}/orders",
    response_model=list[OrderResponse],
    summary="История заказов машины",
    description="Возвращает список всех заказов для указанной машины по её ID.",
    responses={404: {"description": "Машина не найдена"}},
)
async def get_vehicle_orders_history(
    vehicle_id: int = Path(
        ..., description="ID машины, для которой нужно получить историю заказов"
    ),
) -> list[OrderResponse]:
    orders = await VehicleDAO.get_orders_for_vehicle(vehicle_id)

    if not orders:
        logger.warning(f"Не найдены заказы для машины с ID {vehicle_id}")
        raise VehicleNotFoundException

    logger.info(f"История заказов для машины с ID {vehicle_id}: {len(orders)} заказов")

    return orders

import logging

from fastapi import APIRouter, Body, Depends, Path, Response, status
from sqlalchemy.exc import IntegrityError

from app.exceptions import (
    OrderNotFoundException,
    TripSheetConflictException,
    TripSheetNotFoundException,
    VehicleNotFoundException,
)
from app.orders.dao import OrderDAO
from app.trip_sheets.dao import TripSheetDAO
from app.trip_sheets.rb import RBTripSheet
from app.trip_sheets.schemas import TripSheetCreate, TripSheetResponse
from app.vehicles.dao import VehicleDAO

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/tripsheets",
    tags=["Путевые листы"],
)


@router.get(
    "/",
    response_model=list[TripSheetResponse],
    summary="Получить все путевые листы",
    description="Возвращает список всех путевых листов с возможностью фильтрации по параметрам.",
)
async def get_all_trip_sheets(
    request_body: RBTripSheet = Depends(),
) -> list[TripSheetResponse]:
    logger.info("Запрос на получение всех путевых листов")
    trip_sheets = await TripSheetDAO.find_all(**request_body.to_dict())
    if not trip_sheets:
        logger.warning("Путевые листы не найдены")
    logger.info(f"Найдено путевых листов: {len(trip_sheets)}")
    return trip_sheets


@router.get(
    "/{trip_sheet_id}",
    response_model=TripSheetResponse,
    summary="Получить путевой лист по ID",
    description="Возвращает путевой лист по его уникальному идентификатору.",
    responses={404: {"description": "Путевой лист не найден"}},
)
async def get_trip_sheet_by_id(
    trip_sheet_id: int = Path(
        ..., description="ID путевого листа, который нужно получить"
    ),
) -> TripSheetResponse:
    trip_sheet = await TripSheetDAO.find_one_or_none_by_id(trip_sheet_id)
    if not trip_sheet:
        logger.warning(f"Путевой лист с ID {trip_sheet_id} не найден")
        raise TripSheetNotFoundException
    logger.info(f"Получен путевой лист с ID {trip_sheet_id}")
    return trip_sheet


@router.get(
    "/vehicle/{vehicle_id}",
    response_model=list[TripSheetResponse],
    summary="Получить все путевые листы для транспортного средства",
    description="Возвращает все путевые листы для указанного транспортного средства по его ID.",
    responses={404: {"description": "Транспортное средство не найдено"}},
)
async def get_trip_sheets_by_vehicle(
    vehicle_id: int = Path(
        ...,
        description="ID транспортного средства, для которого нужно получить путевые листы",
    ),
) -> list[TripSheetResponse]:
    trip_sheets = await TripSheetDAO.find_all(vehicle_id=vehicle_id)
    if not trip_sheets:
        logger.warning(
            f"Путевые листы для транспортного средства с ID {vehicle_id} не найдены"
        )
        raise TripSheetNotFoundException
    logger.info(
        f"Найдено путевых листов для транспортного средства с ID {vehicle_id}: {len(trip_sheets)}"
    )
    return trip_sheets


@router.post(
    "/",
    response_model=TripSheetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать путевой лист",
    description="Создаёт новый путевой лист для указанного транспортного средства и заказа.",
    responses={400: {"description": "Не удалось создать путевой лист"}},
)
async def create_trip_sheet(
    trip_sheet_data: TripSheetCreate = Body(
        ..., description="Данные для создания нового путевого листа"
    ),
) -> TripSheetResponse:
    vehicle = await VehicleDAO.find_one_or_none_by_id(trip_sheet_data.vehicle_id)
    if not vehicle:
        logger.warning(f"Машина с ID {trip_sheet_data.vehicle_id} не найдена")
        raise VehicleNotFoundException

    order = await OrderDAO.find_one_or_none_by_id(trip_sheet_data.order_id)
    if not order:
        logger.warning(f"Заказ с ID {trip_sheet_data.order_id} не найден")
        raise OrderNotFoundException

    try:
        created_trip_sheet = await TripSheetDAO.add(**trip_sheet_data.model_dump())
        logger.info(f"Создан путевой лист с ID {created_trip_sheet.id}")
        return created_trip_sheet
    except IntegrityError as e:
        logger.error(f"Ошибка при создании путевого листа: {e}")
        raise TripSheetConflictException from e


@router.delete(
    "/{trip_sheet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить путевой лист",
    description="Удаляет путевой лист по ID. Возвращает статус 204, если удаление прошло успешно.",
    responses={404: {"description": "Путевой лист не найден"}},
)
async def delete_trip_sheet(
    trip_sheet_id: int = Path(
        ..., description="ID путевого листа, который нужно удалить"
    ),
) -> Response:
    logger.info(f"Попытка удалить путевой лист с ID {trip_sheet_id}")
    deleted_count = await TripSheetDAO.delete(id=trip_sheet_id)
    if deleted_count == 0:
        logger.warning(f"Путевой лист с ID {trip_sheet_id} не найден для удаления")
        raise TripSheetNotFoundException
    logger.info(f"Удалён путевой лист с ID {trip_sheet_id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

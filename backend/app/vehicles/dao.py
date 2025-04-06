from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.models import Order, TripSheet, Vehicle


class VehicleDAO(BaseDAO):
    model = Vehicle

    @classmethod
    async def get_orders_for_vehicle(cls, vehicle_id: int) -> list[Order]:
        """
        Получить все заказы, связанные с машиной.

        :param vehicle_id: Идентификатор машины.
        :return: Список заказов для машины.
        """
        async with async_session_maker() as session:
            query = (
                select(Order)
                .join(TripSheet, TripSheet.order_id == Order.id)
                .filter(TripSheet.vehicle_id == vehicle_id)
                .options(joinedload(Order.created_by))
            )
            result = await session.execute(query)
            return result.scalars().all()

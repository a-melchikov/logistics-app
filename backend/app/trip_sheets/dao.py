from datetime import datetime

from sqlalchemy.future import select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.models import TripSheet


class TripSheetDAO(BaseDAO):
    model = TripSheet

    @classmethod
    async def check_time_overlap(
        cls, vehicle_id: int, start_time: datetime, end_time: datetime
    ) -> bool:
        async with async_session_maker() as session:
            query = select(cls.model).filter(
                cls.model.vehicle_id == vehicle_id,
                cls.model.start_time < end_time,
                cls.model.end_time > start_time,
            )
            result = await session.execute(query)
            overlapping_trip_sheets = result.scalars().all()

            return len(overlapping_trip_sheets) > 0

from datetime import datetime

from sqlalchemy import and_, select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.enums import OrderStatus
from app.models import Order


class OrderDAO(BaseDAO):
    model = Order

    @classmethod
    async def find_all_filtered(
        cls,
        client_name: str | None = None,
        cost_from: int | None = None,
        cost_to: int | None = None,
        order_date: str | None = None,
        status: OrderStatus | None = None,
    ) -> list[Order]:
        async with async_session_maker() as session:
            query = select(cls.model)
            filters = []

            if client_name:
                filters.append(Order.client_name.ilike(f"%{client_name}%"))

            if cost_from is not None:
                filters.append(cls.model.cost >= cost_from)

            if cost_to is not None:
                filters.append(cls.model.cost <= cost_to)

            if status:
                filters.append(Order.status == status)

            if order_date:
                try:
                    parsed_date = datetime.strptime(order_date, "%Y-%m-%d")
                    start = datetime.combine(parsed_date, datetime.min.time())
                    end = datetime.combine(parsed_date, datetime.max.time())
                    filters.append(Order.order_date.between(start, end))
                except ValueError as e:
                    raise ValueError(
                        "order_date должен быть в формате YYYY-MM-DD"
                    ) from e

            if filters:
                query = query.where(and_(*filters))

            result = await session.execute(query)
            return result.scalars().all()

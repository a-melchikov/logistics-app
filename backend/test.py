import asyncio

from sqlalchemy import select

from app.database.core import async_session_maker
from app.orders.models import Order


async def get_orders():
    async with async_session_maker() as session:
        query = select(Order)
        result = await session.execute(query)
        return list(result.scalars().all())


async def main():
    return await get_orders()


if __name__ == "__main__":
    asyncio.run(main())

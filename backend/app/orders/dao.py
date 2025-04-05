from app.dao.base import BaseDAO
from app.models import Order


class OrderDAO(BaseDAO):
    model = Order

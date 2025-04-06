from app.dao.base import BaseDAO
from app.models import Vehicle


class VehicleDAO(BaseDAO):
    model = Vehicle

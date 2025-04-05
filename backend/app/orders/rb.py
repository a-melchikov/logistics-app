from datetime import datetime

from app.enums import OrderStatus


class RBOrder:
    def __init__(
        self,
        client_name: str | None = None,
        cost: int | None = None,
        order_date: datetime | None = None,
        status: OrderStatus | None = None,
    ):
        self.client_name = client_name
        self.cost = cost
        self.order_date = order_date
        self.status = status

    def to_dict(self) -> dict[str, int]:
        data = {
            "client_name": self.client_name,
            "cost": self.cost,
            "order_date": self.order_date,
            "status": self.status,
        }
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data

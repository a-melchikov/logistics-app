from app.enums import OrderStatus


class RBOrder:
    def __init__(
        self,
        client_name: str | None = None,
        cost_from: int | None = None,
        cost_to: int | None = None,
        order_date: str | None = None,
        status: OrderStatus | None = None,
    ):
        self.client_name = client_name
        self.cost_from = cost_from
        self.cost_to = cost_to
        self.order_date = order_date
        self.status = status

    def to_dict(self) -> dict[str, int]:
        return {
            k: v
            for k, v in {
                "client_name": self.client_name,
                "cost_from": self.cost_from,
                "cost_to": self.cost_to,
                "order_date": self.order_date,
                "status": self.status,
            }.items()
            if v is not None
        }

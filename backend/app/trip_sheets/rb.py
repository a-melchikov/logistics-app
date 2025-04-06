from datetime import datetime


class RBTripSheet:
    def __init__(
        self,
        vehicle_id: int | None = None,
        order_id: int | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ):
        self.vehicle_id = vehicle_id
        self.order_id = order_id
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self) -> dict[str, int | datetime | None]:
        data = {
            "vehicle_id": self.vehicle_id,
            "order_id": self.order_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data

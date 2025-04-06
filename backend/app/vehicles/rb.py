from app.enums import VehicleType


class RBVehicle:
    def __init__(
        self,
        driver_name: str | None = None,
        vehicle_type: VehicleType | None = None,
        license_plate: str | None = None,
    ):
        self.driver_name = driver_name
        self.vehicle_type = vehicle_type
        self.license_plate = license_plate

    def to_dict(self) -> dict[str, int]:
        data = {
            "driver_name": self.driver_name,
            "vehicle_type": self.vehicle_type,
            "license_plate": self.license_plate,
        }
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data

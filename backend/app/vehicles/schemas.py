from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.enums import VehicleType


class VehicleCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    driver_name: str = Field(
        ..., min_length=1, max_length=100, description="ФИО водителя"
    )

    vehicle_type: VehicleType = Field(
        ...,
        description="Тип машины (например, легковой (car), грузовой (truck), фургон (van))",
    )

    license_plate: str = Field(
        ..., min_length=6, max_length=9, description="Государственный номер машины"
    )


class VehicleUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    driver_name: str | None = Field(
        None, min_length=1, max_length=100, description="ФИО водителя"
    )

    vehicle_type: VehicleType | None = Field(
        None,
        description="Тип машины (например, легковой (car), грузовой (truck), фургон (van))",
    )

    license_plate: str | None = Field(
        None, min_length=6, max_length=9, description="Государственный номер машины"
    )


class VehicleResponse(BaseModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    id: int
    driver_name: str
    vehicle_type: VehicleType
    license_plate: str

from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class TripSheetCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vehicle_id: int = Field(
        ...,
        ge=1,
        description="ID транспортного средства, для которого создается путевой лист",
    )

    order_id: int = Field(
        ..., ge=1, description="ID заказа, с которым связан путевой лист"
    )

    start_time: datetime = Field(
        ...,
        description="Дата и время начала рейса в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС",
        json_schema_extra={"example": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    )

    end_time: datetime = Field(
        ...,
        description="Дата и время завершения рейса в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС",
        json_schema_extra={"example": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    )

    @field_validator("vehicle_id", "order_id")
    def validate_positive_ids(cls, value):
        """Проверка, чтобы ID были больше нуля"""
        if value <= 0:
            raise ValueError(
                "ID транспортного средства и заказа должны быть больше нуля."
            )
        return value


class TripSheetUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vehicle_id: int | None = Field(
        None,
        ge=1,
        description="ID транспортного средства для обновления путевого листа",
    )

    order_id: int | None = Field(
        None, ge=1, description="ID заказа для обновления путевого листа"
    )

    start_time: datetime | None = Field(
        None,
        description="Дата и время начала рейса для обновления",
        json_schema_extra={"example": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    )

    end_time: datetime | None = Field(
        None,
        description="Дата и время завершения рейса для обновления",
        json_schema_extra={"example": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    )

    @field_validator("vehicle_id", "order_id")
    def validate_positive_ids(cls, value):
        """Проверка, чтобы ID были больше нуля"""
        if value and value <= 0:
            raise ValueError(
                "ID транспортного средства и заказа должны быть больше нуля."
            )
        return value


class TripSheetResponse(BaseModel):
    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")},
    )

    id: int
    vehicle_id: int
    order_id: int
    start_time: datetime
    end_time: datetime

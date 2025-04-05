from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

from app.enums import OrderStatus


class OrderCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    client_name: str = Field(
        ..., min_length=1, max_length=100, description="Имя или наименование клиента"
    )

    cost: int = Field(..., ge=1, description="Стоимость заказа. Должна быть больше 0")

    order_date: datetime = Field(
        ..., description="Дата и время оформления заказа в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС"
    )

    status: OrderStatus = Field(
        OrderStatus.PENDING,
        description="Статус заказа (pending, in_progress, completed)",
    )

    created_by_id: int = Field(
        ..., ge=1, description="ID пользователя, который создал заказ (диспетчер)"
    )

    @field_validator("client_name")
    def validate_client_name(cls, value):
        if len(value.strip()) == 0:
            raise ValueError("Имя клиента не может быть пустым")
        return value

    @field_validator("cost")
    def validate_cost(cls, value):
        if value <= 0:
            raise ValueError("Стоимость заказа должна быть больше 0")
        return value

    @field_validator("order_date")
    def validate_order_date(cls, value):
        if value > datetime.now():
            raise ValueError("Дата заказа не может быть в будущем")
        return value


class OrderUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    client_name: str | None = Field(
        None, min_length=1, max_length=100, description="Имя или наименование клиента"
    )

    cost: int | None = Field(
        ..., ge=1, description="Стоимость заказа. Должна быть больше 0"
    )

    order_date: datetime | None = Field(
        None, description="Дата и время оформления заказа в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС"
    )

    status: OrderStatus | None = Field(
        OrderStatus.PENDING,
        description="Статус заказа (pending, in_progress, completed)",
    )

    @field_validator("client_name")
    def validate_client_name(cls, value):
        if len(value.strip()) == 0:
            raise ValueError("Имя клиента не может быть пустым")
        return value

    @field_validator("cost")
    def validate_cost(cls, value):
        if value <= 0:
            raise ValueError("Стоимость заказа должна быть больше 0")
        return value

    @field_validator("order_date")
    def validate_order_date(cls, value):
        if value > datetime.now():
            raise ValueError("Дата заказа не может быть в будущем")
        return value


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_name: str
    cost: int
    order_date: datetime
    status: OrderStatus

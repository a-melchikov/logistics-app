import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_pk
from app.trip_sheets.models import TripSheet
from app.users.models import User


class OrderStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Order(Base):
    id: Mapped[int_pk]
    client_name: Mapped[str]
    cost: Mapped[int]
    order_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING,
    )

    created_by_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    created_by: Mapped["User"] = relationship(
        "User",
        back_populates="orders",
    )

    trip_sheet_entries: Mapped["TripSheet"] = relationship(
        "TripSheet",
        back_populates="order",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, client_name={self.client_name}, "
            f"order_date={self.order_date}, status={self.status})"
        )

    def __repr__(self):
        return str(self)

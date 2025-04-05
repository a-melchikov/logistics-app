from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_pk
from app.enums import OrderStatus

if TYPE_CHECKING:
    from app.models import TripSheet, User


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
        back_populates="orders",
    )

    tripsheet_entries: Mapped[list["TripSheet"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, client_name={self.client_name}, "
            f"order_date={self.order_date}, status={self.status})"
        )

    def __repr__(self):
        return str(self)

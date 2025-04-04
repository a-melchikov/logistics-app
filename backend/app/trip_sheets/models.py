from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_pk


class TripSheet(Base):
    id: Mapped[int_pk]
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"),
        nullable=False,
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
    )
    start_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    end_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    vehicle: Mapped["Vehicle"] = relationship(
        "Vehicle",
        back_populates="trip_sheets",
    )
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="trip_sheet_entries",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, vehicle_id={self.vehicle_id}, "
            f"order_id={self.order_id}, start_time={self.start_time}, end_time={self.end_time})"
        )

    def __repr__(self):
        return str(self)

from typing import TYPE_CHECKING

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_pk, str_uniq
from app.enums import VehicleType

if TYPE_CHECKING:
    from app.models import TripSheet


class Vehicle(Base):
    id: Mapped[int_pk]
    driver_name: Mapped[str]
    vehicle_type: Mapped[VehicleType] = mapped_column(
        Enum(VehicleType),
        nullable=False,
    )
    license_plate: Mapped[str_uniq]

    tripsheets: Mapped[list["TripSheet"]] = relationship(
        back_populates="vehicle",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, driver_name={self.driver_name}, "
            f"vehicle_type={self.vehicle_type}, license_plate={self.license_plate})"
        )

    def __repr__(self):
        return str(self)

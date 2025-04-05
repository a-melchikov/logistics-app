from typing import TYPE_CHECKING

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_pk, str_uniq
from app.enums import UserRole

if TYPE_CHECKING:
    from app.models import Order


class User(Base):
    id: Mapped[int_pk]
    username: Mapped[str_uniq]
    hashed_password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        nullable=False,
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="created_by",
    )

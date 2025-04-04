import enum

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_pk, str_uniq


class UserRole(enum.Enum):
    ADMIN = "admin"
    DISPATCHER = "dispatcher"


class User(Base):
    id: Mapped[int_pk]
    username: Mapped[str_uniq]
    hashed_password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        nullable=False,
    )

    orders: Mapped["Order"] = relationship(
        "Order",
        back_populates="created_by",
    )

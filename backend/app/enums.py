import enum


class OrderStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class UserRole(enum.Enum):
    ADMIN = "admin"
    DISPATCHER = "dispatcher"


class VehicleType(enum.Enum):
    TRUCK = "truck"
    VAN = "van"
    CAR = "car"

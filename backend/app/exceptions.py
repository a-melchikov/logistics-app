from fastapi import HTTPException, status

OrderNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Заказ не найден",
)

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Пользователь не найден",
)

VehicleNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Машина не найдена",
)

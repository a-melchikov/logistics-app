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

TripSheetNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Путевой лист не найден",
)

TripSheetConflictException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Не удалось создать путевой лист. Возможно, уже существует путевой лист с таким транспортным средством и заказом.",
)

from fastapi import HTTPException, status


class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")


class TokenNoFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не найден"
        )


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

NoJwtException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не валидный"
)

NoUserIdException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Не найден ID пользователя"
)

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
)

PasswordMismatchException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Пароли не совпадают"
)

IncorrectUsernameOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверное имя пользователя или пароль",
)

InsufficientPermissionsException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав"
)

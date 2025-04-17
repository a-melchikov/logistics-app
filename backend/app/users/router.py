from fastapi import APIRouter, Depends, Response

from app.exceptions import (
    IncorrectUsernameOrPasswordException,
    PasswordMismatchException,
    UserAlreadyExistsException,
)
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UserDAO
from app.users.dependencies import get_current_admin_user, get_current_user
from app.users.models import User
from app.users.schemas import UserAuth, UserRegister

router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post(
    "/register/",
    summary="Регистрация пользователя",
    description="Создаёт нового пользователя в системе. Проверяет, что пароль и подтверждение пароля совпадают.",
    responses={201: {"description": "Пользователь успешно зарегистрирован"}},
)
async def register_user(user_data: UserRegister) -> dict:
    user = await UserDAO.find_one_or_none(username=user_data.username)
    if user:
        raise UserAlreadyExistsException

    if user_data.password != user_data.password_check:
        raise PasswordMismatchException

    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(username=user_data.username, hashed_password=hashed_password)

    return {"message": "Вы успешно зарегистрированы"}


@router.post(
    "/login/",
    summary="Авторизация пользователя",
    description="Авторизует пользователя по логину и паролю, возвращает access token.",
    responses={
        200: {
            "description": "Авторизация успешна",
            "content": {
                "application/json": {
                    "example": {
                        "ok": True,
                        "access_token": "string",
                        "refresh_token": None,
                        "message": "Авторизация успешна",
                    }
                }
            },
        },
        401: {"description": "Неверное имя пользователя или пароль"},
    },
)
async def auth_user(user_data: UserAuth, response: Response):
    check = await authenticate_user(
        username=user_data.username, password=user_data.password
    )
    if check is None:
        raise IncorrectUsernameOrPasswordException

    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {
        "ok": True,
        "access_token": access_token,
        "refresh_token": None,
        "message": "Авторизация успешна",
    }


@router.get(
    "/me/",
    summary="Информация о текущем пользователе",
    description="Возвращает информацию о текущем пользователе. Необходима авторизация.",
)
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.post(
    "/logout/",
    summary="Выход из системы",
    description="Удаляет куку с токеном, таким образом, выходя из системы.",
    responses={200: {"description": "Пользователь успешно вышел из системы"}},
)
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "Пользователь успешно вышел из системы"}


@router.get(
    "/all_users/",
    summary="Получить всех пользователей",
    description="Возвращает список всех пользователей. Доступно только для администратора.",
    responses={200: {"description": "Список пользователей"}},
)
async def get_all_users(user_data: User = Depends(get_current_admin_user)):
    return await UserDAO.find_all()

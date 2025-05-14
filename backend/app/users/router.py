from datetime import timedelta

from fastapi import APIRouter, Depends, Header, Response

from app.config import settings
from app.exceptions import (
    IncorrectUsernameOrPasswordException,
    InvalidRegisterToken,
    PasswordMismatchException,
    UnableUpdateRoleException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.users.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_password_hash,
)
from app.users.dao import UserDAO
from app.users.dependencies import (
    decode_token,
    get_current_admin_user,
    get_current_user,
    get_refresh_token,
)
from app.users.models import User
from app.users.schemas import UpdateUserRole, UserAuth, UserRegister

router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post(
    "/register/",
    summary="Регистрация пользователя",
    description="Создаёт нового пользователя, если передан правильный секретный токен в заголовке.",
    responses={201: {"description": "Пользователь успешно зарегистрирован"}},
)
async def register_user(
    user_data: UserRegister,
    x_register_token: str = Header(...),
) -> dict:
    if x_register_token != settings.REGISTER_SECRET_TOKEN:
        raise InvalidRegisterToken

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
                        "refresh_token": "string",
                        "message": "Авторизация успешна",
                    }
                }
            },
        },
        401: {"description": "Неверное имя пользователя или пароль"},
    },
)
async def auth_user(user_data: UserAuth, response: Response):
    user = await authenticate_user(
        username=user_data.username, password=user_data.password
    )
    if not user:
        raise IncorrectUsernameOrPasswordException

    access_token = create_access_token(
        {"sub": str(user.id)}, expires_delta=timedelta(minutes=15)
    )
    refresh_token = create_refresh_token({"sub": str(user.id)})

    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

    return {
        "ok": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "message": "Авторизация успешна",
    }


@router.post(
    "/refresh/",
    summary="Обновление токена доступа",
    description=(
        "Использует Refresh Token из cookies для создания нового Access Token. "
        "Если Refresh Token валиден и не истек, выдается новый Access Token."
    ),
)
async def refresh_token(response: Response, token: str = Depends(get_refresh_token)):
    payload = decode_token(token)
    user_id = payload.get("sub")

    access_token = create_access_token(
        {"sub": str(user_id)}, expires_delta=timedelta(minutes=15)
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True)

    return {"access_token": access_token}


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
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Пользователь успешно вышел из системы"}


@router.get(
    "/all_users/",
    summary="Получить всех пользователей",
    description="Возвращает список всех пользователей. Доступно только для администратора.",
    responses={200: {"description": "Список пользователей"}},
)
async def get_all_users(user_data: User = Depends(get_current_admin_user)):
    return await UserDAO.find_all()


@router.patch(
    "/update_role/",
    summary="Изменение роли пользователя",
    description="Позволяет администратору изменить роль пользователя по его ID.",
    responses={
        200: {"description": "Роль успешно обновлена"},
        404: {"description": "Пользователь не найден"},
    },
)
async def update_user_role(
    data: UpdateUserRole,
    _: User = Depends(get_current_admin_user),
):
    user = await UserDAO.find_one_or_none_by_id(data.user_id)
    if not user:
        raise UserNotFoundException

    updated_rows = await UserDAO.update({"id": data.user_id}, role=data.new_role)

    if updated_rows == 0:
        raise UnableUpdateRoleException

    return {
        "message": f"Роль пользователя с ID {data.user_id} успешно обновлена на {data.new_role}"
    }

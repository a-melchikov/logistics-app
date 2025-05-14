from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from app.config import get_auth_data
from app.enums import UserRole
from app.exceptions import (
    InsufficientPermissionsException,
    NoUserIdException,
    TokenExpiredException,
    TokenNoFoundException,
    UserNotFoundException,
)
from app.users.dao import UserDAO
from app.users.models import User


def get_bearer_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[len("Bearer ") :]

    token = request.cookies.get("access_token")
    if not token:
        raise TokenNoFoundException
    return token


def get_token(request: Request, token_name: str):
    token = request.cookies.get(token_name)
    if not token:
        raise TokenNoFoundException
    return token


def get_refresh_token(request: Request):
    return get_token(request, "refresh_token")


def decode_token(token: str):
    try:
        auth_data = get_auth_data()
        return jwt.decode(
            token, auth_data["secret_key"], algorithms=[auth_data["algorithm"]]
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или истекший токен",
        ) from e


def get_bearer_token_dependency(request: Request):
    return get_bearer_token(request)


async def get_current_user(token: str = Depends(get_bearer_token_dependency)):
    payload = decode_token(token)
    expire = payload.get("exp")
    if not expire:
        raise TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise NoUserIdException

    user = await UserDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise UserNotFoundException
    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role == UserRole.ADMIN:
        return current_user
    raise InsufficientPermissionsException

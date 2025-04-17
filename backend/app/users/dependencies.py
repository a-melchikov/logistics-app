from datetime import UTC, datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import get_auth_data
from app.enums import UserRole
from app.exceptions import (
    InsufficientPermissionsException,
    NoJwtException,
    NoUserIdException,
    TokenExpiredException,
    TokenNoFoundException,
    UserNotFoundException,
)
from app.users.dao import UserDAO
from app.users.models import User


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise TokenNoFoundException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(
            token, auth_data["secret_key"], algorithms=auth_data["algorithm"]
        )
    except JWTError as e:
        raise NoJwtException from e

    expire: str = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=UTC)
    if (not expire) or (expire_time < datetime.now(UTC)):
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

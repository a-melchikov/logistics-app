from datetime import UTC, datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.config import get_auth_data
from app.users.dao import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, str], expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encoded_jwt = jwt.encode(
        to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"]
    )
    return encoded_jwt


def create_refresh_token(data: dict[str, str]) -> str:
    expires = timedelta(days=7)
    return create_access_token(data, expires)


async def authenticate_user(username: str, password: str):
    user = await UserDAO.find_one_or_none(username=username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

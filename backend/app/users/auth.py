from datetime import UTC, datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.config import get_auth_data
from app.users.dao import UserDAO


def create_access_token(data: dict[str, str]) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=1)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(
        to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"]
    )
    return encode_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str):
    user = await UserDAO.find_one_or_none(username=username)
    if (
        not user
        or verify_password(
            plain_password=password, hashed_password=user.hashed_password
        )
        is False
    ):
        return None
    return user

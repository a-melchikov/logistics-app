from pydantic import BaseModel, Field

from app.enums import UserRole


class UserRegister(BaseModel):
    username: str = Field(..., description="Имя пользователя")
    password: str = Field(
        ..., min_length=5, max_length=50, description="Пароль, от 5 до 50 символов"
    )
    password_check: str = Field(
        ..., min_length=5, max_length=50, description="Пароль, от 5 до 50 символов"
    )


class UserAuth(BaseModel):
    username: str = Field(..., description="Имя пользователя")
    password: str = Field(
        ..., min_length=5, max_length=50, description="Пароль, от 5 до 50 символов"
    )


class UserResponse(BaseModel):
    id: int = Field(..., description="Идентификатор пользователя")
    username: str = Field(..., description="Имя пользователя")
    role: UserRole = Field(..., description="Роль пользователя")


class UpdateUserRole(BaseModel):
    user_id: int = Field(..., description="Идентификатор пользователя")
    new_role: UserRole = Field(..., description="Роль пользователя")

from typing import Self
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator, computed_field
from app.auth.utils import get_password_hash


class SUsername(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя, от 3 до 50 символов")

    model_config = ConfigDict(from_attributes=True)


class SUserAuth(SUsername):
    password: str = Field(min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")


class SUserRegister(SUsername):
    password: str = Field(min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    confirm_password: str = Field(min_length=5, max_length=50, description="Повторите пароль")

    @model_validator(mode="after")
    def check_password(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Пароли не совпадают")
        self.password = get_password_hash(self.password)  # хешируем пароль до сохранения в базе данных
        return self


class SUserAdd(SUsername):
    hashed_password: str = Field(min_length=5, description="Пароль в формате HASH-строки")


class SUserRead(SUsername):
    id: int = Field(..., description="Идентификатор пользователя")

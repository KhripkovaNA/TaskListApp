from datetime import datetime
from typing import Self
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.auth.exceptions import PasswordException
from app.auth.utils import get_password_hash


class SUsername(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя, от 3 до 50 символов")

    model_config = ConfigDict(from_attributes=True)


class SUserAuth(SUsername):
    password: str = Field(min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    fingerprint: str = Field(..., description="Идентификатор устройства или браузера")


class SUserRegister(SUsername):
    password: str = Field(min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    confirm_password: str = Field(min_length=5, max_length=50, description="Повторите пароль")

    @model_validator(mode="after")
    def check_password(self) -> Self:
        if self.password != self.confirm_password:
            raise PasswordException
        self.password = get_password_hash(self.password)  # хешируем пароль до сохранения в базе данных
        return self


class SUserAdd(SUsername):
    password_hash: str = Field(min_length=5, description="Пароль в формате HASH-строки")


class SUserRead(SUsername):
    id: int = Field(..., description="Идентификатор пользователя")


class SAuthData(BaseModel):
    sub: str = Field(..., description="Идентификатор пользователя для токена аутентификации")
    jti: str = Field(..., description="Уникальный идентификатор токена")
    exp: datetime = Field(..., description="Время истечения токена")

    model_config = ConfigDict(from_attributes=True)


class SAuthRead(SAuthData):
    fingerprint: str = Field(..., description="Идентификатор устройства или браузера")


class SAuthAdd(SAuthRead):
    token: str = Field(..., description="Токен доступа для аутентификации")


class SAuthData2(BaseModel):
    fingerprint: str = Field(..., description="Идентификатор устройства или браузера")
    token: str = Field(..., description="Токен доступа для аутентификации")

    model_config = ConfigDict(from_attributes=True)

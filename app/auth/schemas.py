from pydantic import BaseModel, Field, ConfigDict


class SUserAuth(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")


class SUserRegister(SUserAuth):
    password_check: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")


class SUserAdd(BaseModel):
    username: str
    hashed_password: str


class SUserRead(BaseModel):
    id: int = Field(..., description="Идентификатор пользователя")
    username: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")

    model_config = ConfigDict(from_attributes=True)

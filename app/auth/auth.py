from jose import jwt
from datetime import datetime, timedelta, timezone
from app.auth.schemas import SUsername
from app.auth.utils import verify_password, encode_jwt
from app.config import settings
from app.auth.dao import UsersDAO
from app.auth.constants import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(data: dict) -> str:
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=data,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def create_refresh_token(data: dict) -> str:
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=data,
        expire_timedelta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


async def authenticate_user(username: str, password: str):
    user = await UsersDAO.find_one_or_none(filters=SUsername(username=username))
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user

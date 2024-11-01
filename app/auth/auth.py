import uuid
from datetime import datetime, timedelta, timezone
from app.auth.dependencies import get_refresh_token_data
from app.auth.exceptions import NoJwtException
from app.auth.schemas import SUsername, SAuthData2
from app.auth.utils import verify_password, encode_jwt_token
from app.config import settings
from app.auth.dao import UsersDAO, AuthDAO
from app.auth.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": ACCESS_TOKEN_TYPE})
    return encode_jwt_token(to_encode)


async def create_refresh_token(data: dict, fingerprint: str, request) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    jti = str(uuid.uuid4())
    to_encode.update({"exp": expire, "type": REFRESH_TOKEN_TYPE, "jti": jti})
    encode_jwt = encode_jwt_token(to_encode)
    to_encode.update({"fingerprint": fingerprint, "token": encode_jwt})
    await AuthDAO(to_encode, request).delete()
    await AuthDAO(to_encode, request).add()

    return encode_jwt


async def delete_refresh_token(data: SAuthData2, request) -> None:
    token_data = get_refresh_token_data(data.token)
    token_data["fingerprint"] = data.fingerprint
    await AuthDAO(token_data, request).delete()


async def validate_refresh_token(data: SAuthData2, request) -> str:
    token_data = get_refresh_token_data(data.token)
    token_data["fingerprint"] = data.fingerprint
    token = await AuthDAO(token_data, request).find_one_or_none()
    if not token:
        raise NoJwtException

    return str(token_data["sub"])


async def authenticate_user(username: str, password: str):
    user = await UsersDAO.find_one_or_none(filters=SUsername(username=username))
    if not user or verify_password(plain_password=password, hashed_password=user.password_hash) is False:
        return None
    return user

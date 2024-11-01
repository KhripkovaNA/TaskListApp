from fastapi import Request, HTTPException, status, Depends
from jose import JWTError
from datetime import datetime, timezone
from app.auth.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from app.auth.schemas import SUserRead, SAuthRefresh
from app.auth.utils import decode_jwt_token
from app.auth.exceptions import NoJwtException, NoUserIdException
from app.auth.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise NoJwtException
    return token


async def get_current_user(token: str = Depends(get_token)) -> SUserRead:
    try:
        payload = decode_jwt_token(token)
    except JWTError:
        raise NoJwtException

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    token_type = payload.get('type')
    if (not expire) or (expire_time < datetime.now(timezone.utc)) or (token_type != ACCESS_TOKEN_TYPE):
        raise NoJwtException

    user_id: str = payload.get('sub')
    if not user_id:
        raise NoUserIdException

    user = await UsersDAO.find_one_or_none_by_id(data_id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user


def get_refresh_token_data(data: SAuthRefresh) -> dict:
    try:
        payload = decode_jwt_token(data.token)
    except JWTError:
        raise NoJwtException

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    token_type = payload.get('type')
    if (not expire) or (expire_time < datetime.now(timezone.utc)) or (token_type != REFRESH_TOKEN_TYPE):
        raise NoJwtException

    data = dict(
        sub=payload.get('sub'),
        exp=payload.get('exp'),
        jti=payload.get('jti'),
        fingerprint=data.fingerprint
    )
    return data

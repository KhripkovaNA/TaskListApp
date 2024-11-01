from jose import jwt, JWTError
from app.auth.exceptions import NoJwtException
from app.config import settings
from datetime import datetime, timezone
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encode_jwt_token(
    payload: dict,
    private_key: str = settings.SECRET_KEY,
    algorithm: str = settings.ALGORITHM
) -> str:
    to_encode = payload.copy()
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt_token(
    token: str,
    public_key: str = settings.SECRET_KEY,
    algorithm: str = settings.ALGORITHM
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

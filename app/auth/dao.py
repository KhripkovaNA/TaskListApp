from app.dao.base import BaseDAO
from app.auth.models import Users
from app.auth.schemas import SAuthRead, SAuthAdd
from app.config import settings as cfg


class UsersDAO(BaseDAO[Users]):
    model = Users


class AuthDAO:
    def __init__(self, data, request):
        # Инициализация AuthDAO с Redis-соединением и данными
        self.redis = request.state.redis
        self.data = data

    async def add(self):
        # Добавить токен в Redis
        token_data = SAuthAdd.model_validate(self.data)
        key = f"refresh:user:{token_data.sub}:fp:{token_data.fingerprint}:jti:{token_data.jti}"
        value = token_data.token
        await self.redis.set(name=key, value=value, ex=cfg.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600)

    async def find_one_or_none(self):
        # Найти токен в Redis по ключу
        token_data = SAuthRead.model_validate(self.data)
        key = f"refresh:user:{token_data.sub}:fp:{token_data.fingerprint}:jti:{token_data.jti}"
        value = await self.redis.get(key)
        return value.decode() if value else None

    async def delete(self):
        # Удалить все токены, соответствующие шаблону ключа в Redis
        token_data = SAuthRead.model_validate(self.data)
        pattern = f"refresh:user:{token_data.sub}:fp:{token_data.fingerprint}:jti:*" if token_data.fingerprint else "*"
        keys = await self.redis.keys(pattern=pattern)
        if keys:
            await self.redis.delete(*keys)

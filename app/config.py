import os
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

BASEDIR = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int

    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASEDIR, "..", ".env")
    )

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()

log_file_path = os.path.join(BASEDIR, "..",  "log.txt")
logger.add(
    log_file_path, format=settings.FORMAT_LOG, rotation=settings.LOG_ROTATION, retention="7 days", compression="zip"
)

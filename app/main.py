from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from loguru import logger
from redis import asyncio as aioredis
from app.auth.router import router as users_router
from app.tasks.router import router as tasks_router
from app.config import settings as cfg


@asynccontextmanager
async def lifespan(application: FastAPI):
    # Создаем подключение к Redis
    redis = aioredis.from_url(f"redis://{cfg.REDIS_HOST}:{cfg.REDIS_PORT}")
    # Возвращаем объект Redis для использования в приложении
    yield {"redis": redis}


# Инициализация FastAPI приложения
app = FastAPI(
    title="Мои Задачи",
    lifespan=lifespan
)

# Подключение роутеров
app.include_router(users_router)
app.include_router(tasks_router)


# Глобальный обработчик для всех исключений, унаследованных от HTTPException
@app.exception_handler(HTTPException)
async def app_base_exception_handler(request: Request, e: HTTPException):
    # Логирование ошибки с нужной информацией
    logger.error(f"Ошибка: {e.detail} | Код состояния: {e.status_code}")

    return JSONResponse(
        status_code=e.status_code,
        content={"detail": e.detail}
    )


# Обработчик для всех других необработанных ошибок
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, e: Exception):
    logger.error(f"Необработанная ошибка: {e}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка сервера"}
    )

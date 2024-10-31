from fastapi import FastAPI
from app.auth.router import router as users_router
from app.tasks.router import router as tasks_router

# Инициализация FastAPI приложения
app = FastAPI(
    title="Мои Задачи"
)

# Подключение роутеров
app.include_router(users_router)
app.include_router(tasks_router)

from typing import Optional
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.database import connection
from app.tasks.models import Tasks


class TasksDAO(BaseDAO[Tasks]):
    model = Tasks

    @classmethod
    @connection
    async def find_all_by_user_id(cls, user_id: int, session: AsyncSession, filters: Optional[BaseModel] = None):
        # Если фильтры не заданы, получаем все записи пользователя
        query = select(cls.model).filter_by(user_id=user_id)
        if filters:
            # Найти все записи пользователя по фильтрам
            filter_dict = filters.model_dump(exclude_unset=True)
            query = query.filter_by(**filter_dict)
        result = await session.execute(query)
        records = result.scalars().all()
        if not records:
            logger.info(f"Не найдено записей {cls.model.__name__}")
        return records

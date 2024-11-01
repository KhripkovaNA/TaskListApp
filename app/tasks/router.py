from fastapi import APIRouter, Depends, status
from typing import List, Optional
from app.auth.schemas import SUserRead
from app.tasks.schemas import STaskAdd, STaskRead, STaskStatus, STaskCreate
from app.auth.dependencies import get_current_user
from app.tasks.service import create_task_, get_tasks_, update_task_, delete_task_

router = APIRouter(prefix='/tasks', tags=['Задачи'])


@router.post("", response_model=STaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: STaskCreate, user_data: SUserRead = Depends(get_current_user)):
    """
    Создает новую задачу для авторизованного пользователя.
    """
    return await create_task_(task_data, user_data.id)


@router.get("", response_model=List[STaskRead])
async def get_tasks(status: Optional[STaskStatus] = None, user_data: SUserRead = Depends(get_current_user)):
    """
    Получает список всех задач пользователя, с возможностью фильтрации по статусу.
    """
    return await get_tasks_(user_data.id, status)


@router.put("/{task_id}", response_model=STaskRead)
async def update_task(task_id: int, task_data: STaskAdd, user_data: SUserRead = Depends(get_current_user)):
    """
    Обновляет информацию о задаче по ее id.
    """
    return await update_task_(task_id, task_data, user_data.id)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, user_data: SUserRead = Depends(get_current_user)):
    """
    Удаляет задачу по ее id.
    """
    await delete_task_(task_id, user_data.id)
    return {"message": "Задача успешно удалена"}

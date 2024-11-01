from typing import List
from app.tasks.dao import TasksDAO
from app.tasks.exceptions import TaskNotFoundException
from app.tasks.models import Tasks, TaskStatus
from app.tasks.schemas import STaskCreate, STaskAdd, STaskId, STaskStatus, STaskUpdate


async def create_task_(task_data: STaskCreate, user_id: int):
    # Создание новой задачи
    task_data_dict = task_data.model_dump()
    return await TasksDAO.add(values=STaskAdd(user_id=user_id, **task_data_dict))


async def get_tasks_(user_id: int, status: TaskStatus = None) -> List[Tasks]:
    # Получение списка задач
    task_status = STaskStatus(status=status) if status else None
    print(task_status)
    return await TasksDAO.find_all_by_user_id(user_id=user_id, filters=task_status)


async def update_task_(task_id: int, task_data: STaskUpdate, user_id: int):
    # Обновление задачи
    task = await TasksDAO.find_one_or_none_by_id(task_id)
    if not task or task.user_id != user_id:
        raise TaskNotFoundException

    return await TasksDAO.update(filters=STaskId(id=task_id), values=task_data)


async def delete_task_(task_id: int, user_id: int):
    # Удаление задачи
    task = await TasksDAO.find_one_or_none_by_id(task_id)
    if not task or task.user_id != user_id:
        raise TaskNotFoundException

    await TasksDAO.delete(filters=STaskId(id=task_id))

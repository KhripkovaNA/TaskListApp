from app.tasks.dao import TasksDAO
from app.tasks.exceptions import (
    TaskNotAddedException, TasksNotRetrievedException, TaskNotFoundException, CouldNotDeleteTaskException
)
from app.tasks.schemas import STaskCreate, STaskAdd, STaskStatus, STaskRead, STaskId


async def create_task_(task_data: STaskCreate, user_id: int):
    # Создание новой задачи
    try:
        task_data_dict = task_data.model_dump()
        return await TasksDAO.add(values=STaskAdd(user_id=user_id, **task_data_dict))

    except Exception as e:
        raise TaskNotAddedException


async def get_tasks_(user_id: int, status: STaskStatus = None):
    # Получение списка задач
    try:
        if status:
            return await TasksDAO.find_all_by_user_id(user_id=user_id, filters=status)
        else:
            return await TasksDAO.find_all_by_user_id(user_id=user_id)

    except Exception as e:
        raise TasksNotRetrievedException


async def update_task_(task_id: int, task_data: STaskAdd, user_id: int):
    # Обновление задачи
    try:
        task = await TasksDAO.find_one_or_none_by_id(task_id)
        if not task or task.user_id != user_id:
            raise TaskNotFoundException

        return await TasksDAO.update(filters=STaskId(id=task_id), values=task_data)

    except Exception as e:
        raise TasksNotRetrievedException


async def delete_task_(task_id: int, user_id: int):
    # Удаление задачи
    try:
        task = await TasksDAO.find_one_or_none_by_id(task_id)
        if not task or task.user_id != user_id:
            raise TaskNotFoundException

        await TasksDAO.delete(filters=STaskId(id=task_id))

    except Exception as e:
        raise CouldNotDeleteTaskException

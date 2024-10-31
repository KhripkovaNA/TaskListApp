from app.exceptions import AppBaseException
from fastapi import status


class TaskNotAddedException(AppBaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить задачу"


class TasksNotRetrievedException(AppBaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось получить задачи"


class TaskNotFoundException(AppBaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Задача не найдена"


class CouldNotDeleteTaskException(AppBaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось удалить задачу"


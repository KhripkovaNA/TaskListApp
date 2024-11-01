from app.exceptions import AppBaseException
from fastapi import status


class TaskNotFoundException(AppBaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Задача не найдена"

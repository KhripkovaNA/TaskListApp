from app.exceptions import AppBaseException
from fastapi import status


class UserAlreadyExistsException(AppBaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectUsernameOrPasswordException(AppBaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Неверное имя пользователя или пароль'


class TokenExpiredException(AppBaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен истек'


class TokenNoFound(AppBaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен истек'


class NoJwtException(AppBaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен не валидный!'


class NoUserIdException(AppBaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Не найден ID пользователя'


class UserNotFoundException(AppBaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Пользователь не найден'

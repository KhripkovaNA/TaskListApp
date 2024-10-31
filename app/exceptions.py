from fastapi import HTTPException


class AppBaseException(HTTPException):
    # значения по умолчанию
    status_code = 500
    detail = "Ошибка сервера"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

from pydantic import BaseModel, Field, ConfigDict
from app.tasks.models import TaskStatus


class STaskId(BaseModel):
    id: int = Field(..., description="Идентификатор задачи")


class STaskCreate(BaseModel):
    name: str = Field(..., description="Название задачи")
    description: str = Field(..., description="Описание задачи")

    model_config = ConfigDict(from_attributes=True)


class STaskAdd(STaskCreate):
    user_id: int = Field(..., description="Идентификатор пользователя")


class STaskUpdate(STaskCreate):
    status: TaskStatus = Field(..., description="Статус задачи")


class STaskRead(STaskId, STaskCreate):
    status: TaskStatus = Field(..., description="Статус задачи")


class STaskStatus(BaseModel):
    status: TaskStatus = Field(..., description="Статус задачи")




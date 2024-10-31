from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from app.tasks.constants import CREATED, IN_PROGRESS, COMPLETED


class STaskStatus(str, Enum):
    created = CREATED
    in_progress = IN_PROGRESS
    completed = COMPLETED


class STaskCreate(BaseModel):
    name: str = Field(..., description="Название задачи")
    description: str = Field(..., description="Описание задачи")

    model_config = ConfigDict(from_attributes=True)


class STaskAdd(STaskCreate):
    user_id: int = Field(..., description="Идентификатор пользователя")


class STaskRead(STaskCreate):
    id: int = Field(..., description="Идентификатор задачи")
    status: STaskStatus = Field(..., description="Статус задачи")


class STaskWithStatus(BaseModel):
    status: STaskStatus = Field(..., description="Статус задачи")


class STaskId(BaseModel):
    id: int = Field(..., description="Идентификатор задачи")

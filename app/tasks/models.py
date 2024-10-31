from sqlalchemy import String, Integer, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
import enum
from app.tasks.constants import CREATED, IN_PROGRESS, COMPLETED
from app.database import Base


class TaskStatus(enum.Enum):
    created = CREATED
    in_progress = IN_PROGRESS
    completed = COMPLETED


class Tasks(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), nullable=False, default=TaskStatus.created)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    def __str__(self):
        return f"Task-{self.id} {self.name}"

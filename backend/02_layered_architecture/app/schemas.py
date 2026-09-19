from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Priority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class StudyTaskCreate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    title: str = Field(min_length=1, max_length=100)
    priority: Priority = Priority.MEDIUM


class StudyTaskResponse(BaseModel):
    id: int
    title: str
    priority: Priority
    completed: bool

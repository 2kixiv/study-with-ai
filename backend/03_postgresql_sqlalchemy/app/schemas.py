from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StudyNoteCreate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    title: str = Field(min_length=1, max_length=100)

    content: str = Field(min_length=1, max_length=5000)


class StudyNoteResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    title: str
    content: str
    created_at: datetime

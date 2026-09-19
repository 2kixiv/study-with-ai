from pydantic import BaseModel, Field


class StudyRecordCreate(BaseModel):
    """학습 기록 생성 요청."""

    topic: str = Field(min_length=1, max_length=100)
    minutes: int = Field(ge=1, le=720)

    model_config = {
        "str_strip_whitespace": True,
    }


class StudyRecordResponse(BaseModel):
    """클라이언트에 반환하는 학습 기록."""

    id: int
    topic: str
    minutes: int
    completed: bool


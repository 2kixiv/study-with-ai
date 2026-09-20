from datetime import datetime
from typing import Self
from pydantic import BaseModel, ConfigDict, Field, model_validator


class PostCreate(BaseModel):
    # TODO: 추가 필드를 금지하고 문자열 공백을 제거하세요.
    model_config = ConfigDict()
    # TODO: title 1~200자, content 1~10000자로 제한하세요.
    title: str
    content: str


class PostUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1, max_length=10000)

    @model_validator(mode="after")
    def require_field(self) -> Self:
        # TODO: 두 필드가 모두 None이면 ValueError를 발생시키세요.
        return self


class AuthorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class PostResponse(BaseModel):
    # TODO: ORM 객체 변환을 허용하세요.
    model_config = ConfigDict()
    id: int
    title: str
    content: str
    author: AuthorResponse
    created_at: datetime
    updated_at: datetime


class PostPage(BaseModel):
    items: list[PostResponse]
    total: int
    page: int
    size: int
    pages: int

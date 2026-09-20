from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint, func, true
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=true(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    posts: Mapped[list["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: title은 VARCHAR(200), content는 TEXT로 정의하세요.
    title: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    # TODO: users.id 외래 키와 DB CASCADE 삭제를 설정하세요.
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # TODO: created_at과 updated_at의 DB 기본값 및 updated_at의 갱신값을 설정하세요.
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    author: Mapped[User] = relationship(back_populates="posts")

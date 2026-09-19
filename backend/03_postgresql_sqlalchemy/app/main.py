from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

import app.models  # ORM 모델을 Base metadata에 등록합니다.
from app.database import Base, engine, get_db
from app.exceptions import StudyNoteNotFoundError
from app.router import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(title="PostgreSQL Study Note API", lifespan=lifespan)
app.include_router(router)


@app.get("/health")
def health(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return { "status": "ok", "database": "ok" }


@app.exception_handler(StudyNoteNotFoundError)
async def handle_not_found(
    request: Request, exc: StudyNoteNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )

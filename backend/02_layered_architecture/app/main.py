from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import (
    DuplicateActiveTaskError,
    StudyTaskAlreadyCompletedError,
    StudyTaskNotFoundError,
)
from app.router import router

app = FastAPI(title="Layered Study Task API")
app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(StudyTaskNotFoundError)
async def handle_not_found(
    request: Request, exc: StudyTaskNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(DuplicateActiveTaskError)
async def handle_duplicate(
    request: Request, exc: DuplicateActiveTaskError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


@app.exception_handler(StudyTaskAlreadyCompletedError)
async def handle_already_completed(
    request: Request, exc: StudyTaskAlreadyCompletedError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import DuplicateEmailError, UserNotFoundError
from app.router import router

app = FastAPI(title="Alembic User API")
app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(UserNotFoundError)
async def handle_not_found(
    request: Request, exc: UserNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(DuplicateEmailError)
async def handle_duplicate(
    request: Request, exc: DuplicateEmailError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


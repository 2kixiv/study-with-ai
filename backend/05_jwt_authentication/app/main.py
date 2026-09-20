from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import (
    DuplicateEmailError,
    InactiveUserError,
    InvalidCredentialsError,
)
from app.router import auth_router, user_router

app = FastAPI(title="JWT Authentication API")
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(DuplicateEmailError)
async def handle_duplicate(
    request: Request, exc: DuplicateEmailError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


@app.exception_handler(InvalidCredentialsError)
async def handle_invalid_credentials(
    request: Request, exc: InvalidCredentialsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(InactiveUserError)
async def handle_inactive(
    request: Request, exc: InactiveUserError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc)},
    )


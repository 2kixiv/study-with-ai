from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.exceptions import DuplicateEmailError, InactiveUserError, InvalidCredentialsError, NotPostOwnerError, PostNotFoundError
from app.router import auth_router, post_router

app = FastAPI(title="Posts Relationships API")
app.include_router(auth_router)
app.include_router(post_router)


@app.get("/health")
def health() -> dict[str, str]: return {"status": "ok"}


def error_response(status_code: int, exc: Exception, headers: dict[str, str] | None = None) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"detail": str(exc)}, headers=headers)


@app.exception_handler(DuplicateEmailError)
async def duplicate(request: Request, exc: DuplicateEmailError): return error_response(409, exc)
@app.exception_handler(InvalidCredentialsError)
async def invalid(request: Request, exc: InvalidCredentialsError): return error_response(401, exc, {"WWW-Authenticate": "Bearer"})
@app.exception_handler(InactiveUserError)
async def inactive(request: Request, exc: InactiveUserError): return error_response(403, exc)
@app.exception_handler(PostNotFoundError)
async def post_missing(request: Request, exc: PostNotFoundError): return error_response(404, exc)
@app.exception_handler(NotPostOwnerError)
async def not_owner(request: Request, exc: NotPostOwnerError): return error_response(403, exc)


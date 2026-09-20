from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import ActiveUserDependency, ServiceDependency
from app.schemas import TokenResponse, UserRegister, UserResponse
from app.security import create_access_token

auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
user_router = APIRouter(prefix="/api/v1/users", tags=["users"])


@auth_router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(data: UserRegister, service: ServiceDependency) -> UserResponse:
    return service.register(data)


@auth_router.post("/token", response_model=TokenResponse)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: ServiceDependency,
) -> TokenResponse:
    user = service.authenticate(form.username, form.password)
    return TokenResponse(access_token=create_access_token(user.id))


@user_router.get("/me", response_model=UserResponse)
def read_me(user: ActiveUserDependency) -> UserResponse:
    return user


@user_router.post("/me/deactivate", response_model=UserResponse)
def deactivate_me(
    user: ActiveUserDependency,
    service: ServiceDependency,
) -> UserResponse:
    return service.deactivate(user)


from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_access_token
from app.auth_schemas import RegisterRequest, TokenResponse
from app.dependencies import ActiveUserDependency, AuthRepositoryDependency, PostServiceDependency
from app.models import User
from app.post_schemas import PostCreate, PostPage, PostResponse, PostUpdate

auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
post_router = APIRouter(prefix="/api/v1/posts", tags=["posts"])


@auth_router.post("/register", status_code=201)
def register(data: RegisterRequest, repository: AuthRepositoryDependency) -> dict:
    user = repository.register(str(data.email), data.name, data.password)
    return {"id": user.id, "email": user.email, "name": user.name}


@auth_router.post("/token", response_model=TokenResponse)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], repository: AuthRepositoryDependency) -> TokenResponse:
    user = repository.authenticate(form.username, form.password)
    return TokenResponse(access_token=create_access_token(user.id))


@post_router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(data: PostCreate, user: ActiveUserDependency, service: PostServiceDependency) -> PostResponse:
    return service.create(data, user)


@post_router.get("", response_model=PostPage)
def list_posts(
    service: PostServiceDependency,
    q: str | None = Query(default=None, max_length=200),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
) -> PostPage:
    return service.list_posts(query=q, page=page, size=size)


@post_router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, service: PostServiceDependency) -> PostResponse:
    return service.get(post_id)


@post_router.patch("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, data: PostUpdate, user: ActiveUserDependency, service: PostServiceDependency) -> PostResponse:
    return service.update(post_id, data, user)


@post_router.delete("/{post_id}", status_code=204, response_class=Response)
def delete_post(post_id: int, user: ActiveUserDependency, service: PostServiceDependency) -> Response:
    service.delete(post_id, user)
    return Response(status_code=204)


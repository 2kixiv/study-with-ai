from fastapi import APIRouter, Query, Response, status

from app.dependencies import ServiceDependency
from app.schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, service: ServiceDependency) -> UserResponse:
    return service.create(data)


@router.get("", response_model=list[UserResponse])
def list_users(
    service: ServiceDependency,
    is_active: bool | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[UserResponse]:
    return service.list_users(
        is_active=is_active,
        limit=limit,
        offset=offset,
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: ServiceDependency) -> UserResponse:
    return service.get(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int, data: UserUpdate, service: ServiceDependency
) -> UserResponse:
    return service.update(user_id, data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_user(user_id: int, service: ServiceDependency) -> Response:
    service.delete(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


from app.exceptions import NotPostOwnerError, PostNotFoundError
from app.models import Post, User
from app.post_repository import PostRepository
from app.post_schemas import PostCreate, PostPage, PostUpdate


class PostService:
    def __init__(self, repository: PostRepository) -> None:
        self._repository = repository

    def create(self, data: PostCreate, user: User) -> Post:
        # TODO: 현재 사용자의 ID로 게시글을 생성하세요.
        raise NotImplementedError

    def list_posts(self, *, query: str | None, page: int, size: int) -> PostPage:
        # TODO: 저장소 결과와 ceil을 이용해 PostPage를 만드세요. total이 0이면 pages는 0입니다.
        raise NotImplementedError

    def get(self, post_id: int) -> Post:
        # TODO: 없으면 PostNotFoundError를 발생시키세요.
        raise NotImplementedError

    def update(self, post_id: int, data: PostUpdate, user: User) -> Post:
        # TODO: 존재 여부 확인 후 작성자가 아니면 NotPostOwnerError를 발생시키세요.
        raise NotImplementedError

    def delete(self, post_id: int, user: User) -> None:
        # TODO: 존재 여부와 작성자 권한을 확인한 뒤 삭제하세요.
        raise NotImplementedError

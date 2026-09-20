from sqlalchemy.orm import Session
from app.models import Post
from app.post_schemas import PostCreate, PostUpdate


class PostRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, data: PostCreate, author_id: int) -> Post:
        # TODO: 게시글을 저장하고 작성자까지 로딩해 반환하세요.
        raise NotImplementedError

    def list_page(self, *, query: str | None, page: int, size: int) -> tuple[list[Post], int]:
        # TODO: DB에서 검색, 전체 개수, 최신순 페이지네이션, 작성자 eager loading을 수행하세요.
        raise NotImplementedError

    def get(self, post_id: int) -> Post | None:
        # TODO: 작성자를 eager loading해 한 건 또는 None을 반환하세요.
        raise NotImplementedError

    def update(self, post: Post, data: PostUpdate) -> Post:
        # TODO: 요청에 포함된 필드만 수정하고 commit → refresh하세요.
        raise NotImplementedError

    def delete(self, post: Post) -> None:
        # TODO: 삭제하고 commit하세요.
        raise NotImplementedError

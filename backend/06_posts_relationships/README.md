# 06. 게시글 관계·검색·페이지네이션

## 목표

기존 사용자 인증에 게시글을 추가합니다. PostgreSQL 외래 키, SQLAlchemy 관계,
작성자 소유권, 검색, 페이지네이션, N+1 문제를 함께 연습합니다.

## 준비

```bash
cd backend/06_posts_relationships
docker compose up -d --wait
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 문제

`TODO`를 구현해 게시글 API를 완성하세요. 인증 관련 코드는 5번 과제의 완성된
기반 코드로 제공됩니다.

### 데이터 관계

```text
users (1) ──────< posts (N)
```

`posts` 테이블 요구사항:

| 열 | 조건 |
|---|---|
| `id` | 정수 기본 키 |
| `title` | `VARCHAR(200)`, `NOT NULL` |
| `content` | `TEXT`, `NOT NULL` |
| `author_id` | `users.id` 외래 키, `NOT NULL`, 사용자 삭제 시 CASCADE |
| `created_at` | 타임존 포함, DB 기본값 `now()` |
| `updated_at` | 타임존 포함, DB 기본값 `now()` |

`0001`은 사용자 테이블을 만들며 완성되어 있습니다. `0002_create_posts.py`의
upgrade/downgrade를 구현하세요.

### API

| 기능 | 요청 | 인증 | 성공 |
|---|---|---|---|
| 생성 | `POST /api/v1/posts` | 필요 | 201 |
| 목록 | `GET /api/v1/posts` | 불필요 | 200 |
| 단일 조회 | `GET /api/v1/posts/{id}` | 불필요 | 200 |
| 수정 | `PATCH /api/v1/posts/{id}` | 작성자 | 200 |
| 삭제 | `DELETE /api/v1/posts/{id}` | 작성자 | 204 |

생성 입력:

```json
{"title": "FastAPI", "content": "관계와 권한을 공부한다."}
```

- 제목은 공백 제거 후 1~200자입니다.
- 본문은 공백 제거 후 1~10000자입니다.
- 수정 요청에는 제목과 본문 중 적어도 하나가 있어야 합니다.
- 작성자는 토큰의 현재 사용자로 결정하며 요청 본문에서 받지 않습니다.

응답에는 작성자 요약이 포함됩니다. 이메일과 비밀번호 해시는 노출하지 않습니다.

```json
{
  "id": 1,
  "title": "FastAPI",
  "content": "관계와 권한을 공부한다.",
  "author": {"id": 1, "name": "Learner"},
  "created_at": "...",
  "updated_at": "..."
}
```

### 목록·검색·페이지네이션

```text
GET /api/v1/posts?q=fastapi&page=1&size=20
```

- `q`: 선택값, 제목 또는 본문에서 대소문자를 무시한 부분 검색
- `page`: 1 이상, 기본 1
- `size`: 1~100, 기본 20
- 최신 글부터 `id` 내림차순 정렬
- `total`: 검색 조건에 맞는 전체 개수
- `pages`: `ceil(total / size)`, 결과가 없으면 0

```json
{"items": [], "total": 0, "page": 1, "size": 20, "pages": 0}
```

목록에서 각 작성자를 가져오기 위해 글마다 추가 쿼리를 실행하면 안 됩니다.
`joinedload()` 등의 eager loading을 사용해 목록 쿼리와 함께 작성자를 로딩하세요.

### 오류와 권한

- 없는 게시글: `404`, `{"detail": "Post not found"}`
- 다른 사용자의 수정·삭제: `403`, `{"detail": "Not post owner"}`
- 인증 없음·잘못된 토큰: `401`
- 비활성 사용자: `403`

존재 여부를 먼저 확인한 뒤 소유권을 검사합니다. 따라서 존재하지 않는 글은
작성자가 누구든 `404`입니다.

## 구현 대상

- `alembic/versions/0002_create_posts.py`
- `app/models.py`의 `Post`
- `app/post_schemas.py`
- `app/post_repository.py`
- `app/post_service.py`

라우터와 인증 의존성은 완성되어 있습니다.

## 제약

- 테스트를 수정하지 않습니다.
- 작성자 ID를 요청 본문에서 받지 않습니다.
- 저장소에서 `HTTPException`을 사용하지 않습니다.
- 페이지네이션한 결과 길이를 `total`로 사용하지 않습니다.
- Python으로 전체 행을 불러온 뒤 검색·페이지네이션하지 않습니다.
- 빈 `except:`를 사용하지 않습니다.

## 실행과 채점

```bash
pytest -q
```

테스트가 마이그레이션을 적용합니다. 서버를 직접 실행할 때는:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

## 권장 순서

1. `models.py`
2. `0002_create_posts.py`
3. `post_schemas.py`
4. `post_repository.py`
5. `post_service.py`
6. 전체 테스트

## 완료 후 생각해 볼 질문

- DB 외래 키와 ORM `relationship()`은 각각 무엇을 보장할까요?
- `count` 쿼리와 목록 쿼리를 분리하는 이유는 무엇일까요?
- 소유권 검사를 라우터가 아니라 서비스에서 하는 이유는 무엇일까요?
- eager loading을 하지 않으면 목록 크기에 따라 쿼리가 어떻게 증가할까요?


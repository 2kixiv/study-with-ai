# 04. Alembic 사용자 CRUD

## 목표

Alembic으로 PostgreSQL 스키마 변경 이력을 관리하고 사용자 CRUD를 구현합니다.
DB 유일 제약 위반을 안전하게 처리하고, 실패한 트랜잭션을 롤백하여 세션을 다시
사용할 수 있게 만드는 것까지 연습합니다.

```text
HTTP → router → service → repository → SQLAlchemy → PostgreSQL
                                      │
                                  Alembic schema
```

## 실행 준비

```bash
cd backend/04_user_crud_migrations
docker compose up -d --wait
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 문제

`app`과 `alembic/versions` 아래의 `TODO`를 구현해 사용자 CRUD를 완성하세요.

### 1. Alembic 마이그레이션

초기 리비전의 `upgrade()`에서 `users` 테이블을 만들고 `downgrade()`에서
제거합니다. 애플리케이션에서는 `Base.metadata.create_all()`을 사용하지 않습니다.

`users` 테이블 조건:

| 열 | 조건 |
|---|---|
| `id` | 정수 기본 키, 자동 증가 |
| `email` | `VARCHAR(320)`, `NOT NULL`, 유일 제약 이름 `uq_users_email` |
| `name` | `VARCHAR(50)`, `NOT NULL` |
| `is_active` | `BOOLEAN`, `NOT NULL`, 서버 기본값 `true` |
| `created_at` | 타임존 포함 시각, `NOT NULL`, 서버 기본값 `now()` |
| `updated_at` | 타임존 포함 시각, `NOT NULL`, 서버 기본값 `now()` |

ORM 모델도 마이그레이션 스키마와 일치해야 합니다.

마이그레이션 명령:

```bash
alembic upgrade head
alembic current
alembic downgrade -1
alembic upgrade head
```

### 2. API

| 기능 | 메서드와 경로 | 성공 상태 |
|---|---|---|
| 상태 확인 | `GET /health` | 200 |
| 사용자 생성 | `POST /api/v1/users` | 201 |
| 목록 | `GET /api/v1/users` | 200 |
| 단일 조회 | `GET /api/v1/users/{user_id}` | 200 |
| 수정 | `PATCH /api/v1/users/{user_id}` | 200 |
| 삭제 | `DELETE /api/v1/users/{user_id}` | 204 |

목록 API는 다음 쿼리를 지원합니다.

- `is_active`: 생략하면 전체, `true` 또는 `false`면 상태 필터
- `limit`: 1~100, 기본값 20
- `offset`: 0 이상, 기본값 0

목록은 `id` 오름차순입니다.

### 3. 입력과 오류

- 이메일은 유효한 형식이어야 하며 저장 전 소문자로 변환합니다.
- 이름은 공백 제거 후 1~50자입니다.
- 수정은 `name`, `is_active` 중 적어도 하나를 포함해야 합니다.
- 알 수 없는 필드는 허용하지 않습니다.
- 없는 사용자의 조회·수정·삭제는 `404`, 본문은
  `{"detail": "User not found"}`입니다.
- 중복 이메일은 `409`, 본문은
  `{"detail": "Email already exists"}`입니다.

중복 이메일은 사전 조회만으로 처리하면 안 됩니다. 동시에 같은 이메일을 생성할
수 있으므로 DB의 유일 제약 위반인 `IntegrityError`를 처리해야 합니다. 실패한
세션에는 반드시 `rollback()`을 호출한 뒤 도메인 예외로 변환하세요.

## 파일별 구현 대상

- `alembic/versions/0001_create_users.py`: upgrade/downgrade
- `app/models.py`: 마이그레이션과 일치하는 ORM 모델
- `app/schemas.py`: 입력 검증, 이메일 정규화, 부분 수정 검증
- `app/repository.py`: CRUD, 필터·페이지네이션, 롤백

나머지 파일은 완성되어 있습니다. 계층이 연결되는 흐름을 읽어보세요.

## 제약

- 테스트와 Alembic 환경 설정을 수정하지 않습니다.
- `create_all()`과 SQLite를 사용하지 않습니다.
- 이메일 중복을 `SELECT` 후 `INSERT`하는 방식으로만 처리하지 않습니다.
- 빈 `except:`를 사용하지 않습니다.
- SQL 문자열을 직접 조합하지 않습니다.
- 저장소에서 `HTTPException`을 사용하지 않습니다.

## 채점

컨테이너가 실행 중인 상태에서:

```bash
pytest -q
```

테스트가 마이그레이션을 적용하므로 별도로 `alembic upgrade head`를 하지 않아도
되지만, 서버를 직접 실행하기 전에는 반드시 적용해야 합니다.

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

## 권장 구현 순서

1. `models.py`
2. `0001_create_users.py`
3. `alembic upgrade head`와 `alembic current`
4. `schemas.py`
5. `repository.py`
6. `pytest -vv -x --tb=short`

## 완료 후 생각해 볼 질문

- ORM 모델만 수정해도 실제 테이블이 바뀌지 않는 이유는 무엇일까요?
- 중복 이메일을 사전 조회만으로 막을 수 없는 이유는 무엇일까요?
- `IntegrityError` 후 롤백하지 않으면 세션은 어떤 상태가 될까요?
- `PATCH` 요청 모델의 모든 필드가 선택적이어야 하는 이유는 무엇일까요?


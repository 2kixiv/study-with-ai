# 03. PostgreSQL 학습 노트 API

## 목표

Docker Compose로 PostgreSQL을 실행하고 SQLAlchemy 2.x를 사용해 데이터를
영속적으로 저장합니다. 2번 과제의 계층 구조는 유지하되 이번 과제에서는
데이터베이스 연결, ORM 모델, 세션 생명주기, 저장소 구현에 집중합니다.

> 이번 과제에서는 학습 목적으로 `create_all()`을 사용합니다. 실제 프로젝트의
> 스키마 변경을 관리하는 마이그레이션은 다음 과제에서 다룹니다.

## 구조

```text
HTTP → router → service → repository → SQLAlchemy Session → PostgreSQL
                                      ↑
                                 dependencies.py
```

## 실행 준비

과제 폴더에서 다음 명령을 실행합니다.

```bash
cd backend/03_postgresql_sqlalchemy
docker compose up -d --wait
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

PostgreSQL은 호스트의 `5433` 포트에서 실행됩니다. 컨테이너 상태는 다음으로
확인할 수 있습니다.

```bash
docker compose ps
```

## 문제

`app` 아래의 `TODO`를 구현하여 PostgreSQL 기반 학습 노트 API를 완성하세요.

학습 노트 응답은 다음 형태입니다.

```json
{
  "id": 1,
  "title": "SQLAlchemy Session",
  "content": "세션의 역할을 정리한다.",
  "created_at": "2026-09-19T10:30:00+00:00"
}
```

### API 요구사항

| 기능 | 메서드와 경로 | 성공 상태 코드 |
|---|---|---|
| 앱·DB 상태 확인 | `GET /health` | 200 |
| 노트 생성 | `POST /api/v1/notes` | 201 |
| 전체 노트 조회 | `GET /api/v1/notes` | 200 |
| 단일 노트 조회 | `GET /api/v1/notes/{note_id}` | 200 |
| 노트 삭제 | `DELETE /api/v1/notes/{note_id}` | 204 |

상태 확인 응답은 다음과 같습니다.

```json
{"status": "ok", "database": "ok"}
```

없는 노트의 조회와 삭제는 `404`와 다음 본문을 반환합니다.

```json
{"detail": "Study note not found"}
```

### 입력 검증

- `title`은 앞뒤 공백 제거 후 1~100자입니다.
- `content`는 앞뒤 공백 제거 후 1~5000자입니다.
- 알 수 없는 요청 필드는 허용하지 않습니다.

### 테이블 요구사항

테이블 이름은 `study_notes`이며 다음 열을 가집니다.

| 열 | PostgreSQL/SQLAlchemy 조건 |
|---|---|
| `id` | 정수 기본 키, DB 자동 증가 |
| `title` | `VARCHAR(100)`, `NOT NULL` |
| `content` | `TEXT`, `NOT NULL` |
| `created_at` | 타임존 포함 시각, `NOT NULL`, DB 서버 기본값 `now()` |

목록은 `id` 오름차순으로 반환합니다.

## 파일별 구현 대상

- `schemas.py`: 입력 제약과 ORM 응답 변환 설정
- `models.py`: `study_notes` ORM 모델 열 설정
- `database.py`: 요청마다 세션을 제공하고 항상 닫는 의존성
- `repository.py`: SQLAlchemy를 이용한 생성·조회·삭제
- `main.py`: 시작 시 테이블 생성과 `SELECT 1` DB 상태 확인

`router.py`, `service.py`, `dependencies.py`는 계층 연결의 예시로 완성되어
있습니다. 흐름을 읽어보되 수정할 필요는 없습니다.

## SQLAlchemy 2.x 힌트

조회에는 `select()`를 사용합니다.

```python
statement = select(SomeModel).order_by(SomeModel.id)
result = session.scalars(statement)
items = list(result.all())
```

생성된 ID와 DB 기본값을 가져오려면 저장 후 다음 과정이 필요합니다.

```text
add → commit → refresh
```

세션 의존성은 `yield`와 `finally`를 이용해 요청이 끝난 뒤 성공·실패와 관계없이
세션을 닫아야 합니다.

## 제약

- 테스트 파일과 Docker Compose 설정은 수정하지 않습니다.
- SQLite로 변경하지 않습니다.
- 메모리 리스트나 딕셔너리에 노트를 저장하지 않습니다.
- 저장소에서 `HTTPException`을 사용하지 않습니다.
- SQL 문자열을 직접 조합하지 않고 SQLAlchemy 표현식을 사용합니다.
- 삭제 후 트랜잭션을 커밋합니다.

## 채점

PostgreSQL 컨테이너가 실행 중인 상태에서:

```bash
pytest -q
```

서버를 직접 실행하려면:

```bash
uvicorn app.main:app --reload
```

종료할 때는 다음 명령으로 컨테이너만 내릴 수 있습니다. 데이터 볼륨은 유지됩니다.

```bash
docker compose down
```

## 권장 구현 순서

1. `schemas.py`
2. `models.py`
3. `database.py`
4. `repository.py`
5. `main.py`의 lifespan
6. `main.py`의 health check
7. 전체 테스트

## 완료 후 생각해 볼 질문

- `commit()`과 `refresh()`는 각각 왜 필요할까요?
- 요청마다 새 세션을 만들고 닫아야 하는 이유는 무엇일까요?
- 앱 재시작 후에도 데이터가 남는 이유는 무엇일까요?
- `create_all()`만으로 운영 중인 테이블 변경을 관리하기 어려운 이유는
  무엇일까요?


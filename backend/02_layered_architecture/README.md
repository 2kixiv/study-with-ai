# 02. 계층형 학습 할 일 API

## 목표

첫 과제에서는 라우터가 저장소를 직접 호출했습니다. 이번에는 애플리케이션을
`router → service → repository`로 나누고 FastAPI의 `Depends`를 이용해 각
계층을 연결합니다.

```text
HTTP 요청 → router → service → repository → 메모리
              │          │
          HTTP 표현   비즈니스 규칙
```

## 실행 준비

```bash
cd backend/02_layered_architecture
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 문제

`app` 아래의 `TODO`를 구현해 학습 할 일 API를 완성하세요.

학습 할 일은 다음 형태입니다.

```json
{
  "id": 1,
  "title": "FastAPI Depends 익히기",
  "priority": "high",
  "completed": false
}
```

우선순위는 `low`, `medium`, `high` 중 하나이며 생략하면 `medium`입니다.

### API 요구사항

| 기능 | 메서드와 경로 | 성공 상태 코드 |
|---|---|---|
| 상태 확인 | `GET /health` | 200 |
| 생성 | `POST /api/v1/study-tasks` | 201 |
| 목록 | `GET /api/v1/study-tasks` | 200 |
| 단일 조회 | `GET /api/v1/study-tasks/{task_id}` | 200 |
| 완료 | `PATCH /api/v1/study-tasks/{task_id}/complete` | 200 |
| 삭제 | `DELETE /api/v1/study-tasks/{task_id}` | 204 |

목록 API는 선택적인 `completed` 쿼리를 지원합니다.

```text
GET /api/v1/study-tasks?completed=false
```

### 입력 검증

- `title`은 앞뒤 공백을 제거한 뒤 1~100자여야 합니다.
- `priority`에 허용되지 않은 값이 들어오면 `422`를 반환합니다.
- 알 수 없는 요청 필드는 허용하지 않습니다.

### 비즈니스 규칙

- 완료되지 않은 작업 중 같은 제목은 대소문자를 무시하고 중복될 수 없습니다.
- 중복이면 `409`와 `{"detail": "Active task with this title already exists"}`를
  반환합니다.
- 완료된 작업과 같은 제목으로는 새 작업을 만들 수 있습니다.
- 이미 완료된 작업을 다시 완료하면 `409`와
  `{"detail": "Study task is already completed"}`를 반환합니다.
- 없는 작업의 조회·완료·삭제는 `404`와
  `{"detail": "Study task not found"}`를 반환합니다.

## 계층별 책임

- `schemas.py`: API 입력 검증과 응답 형태
- `repository.py`: 메모리 저장·조회·삭제만 담당
- `service.py`: 중복, 완료 여부, 존재 여부와 같은 비즈니스 규칙
- `router.py`: 요청을 서비스에 전달하고 결과를 반환
- `dependencies.py`: 저장소와 서비스를 생성하고 FastAPI에 연결
- `main.py`: 앱 조립과 도메인 오류의 HTTP 변환

서비스가 `HTTPException`을 직접 발생시키거나 저장소가 HTTP 상태 코드를 알게
만들지 마세요.

## 제약

- 테스트 파일은 수정하지 않습니다.
- 라우터에서 저장소를 직접 import하거나 접근하지 않습니다.
- 서비스에서 FastAPI의 `HTTPException`을 사용하지 않습니다.
- 모듈 수준의 전역 리스트나 딕셔너리를 추가하지 않습니다.
- 제공된 의존성 함수와 도메인 예외를 사용합니다.

## 실행과 채점

```bash
pytest -q
uvicorn app.main:app --reload
```

## 권장 구현 순서

1. `schemas.py`
2. `repository.py`
3. `service.py`
4. `dependencies.py`
5. `router.py`
6. 전체 테스트 실행

## 완료 후 생각해 볼 질문

- 중복 검사 규칙이 저장소가 아니라 서비스에 있어야 하는 이유는 무엇일까요?
- 테스트가 실제 전역 저장소 대신 새로운 저장소를 넣을 수 있는 이유는
  무엇일까요?
- PostgreSQL 저장소로 교체한다면 어느 계층이 가장 많이 바뀔까요?


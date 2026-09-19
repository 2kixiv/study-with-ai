# 01. 학습 기록 API

## 목표

FastAPI의 라우팅, 요청/응답 모델, HTTP 상태 코드, 입력 검증을 익힙니다.
첫 과제에서는 데이터베이스 대신 메모리를 사용합니다. PostgreSQL은 이후
과제에서 같은 저장소 역할을 대체하며 도입합니다.

## 실행 준비

```bash
cd backend/01_fastapi_basics
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 문제

`app/main.py`, `app/schemas.py`, `app/repository.py`의 `TODO`를 구현하여 아래
API를 완성하세요.

### 1. 상태 확인

`GET /health`

- 상태 코드: `200 OK`
- 응답: `{"status": "ok"}`

### 2. 학습 기록 생성

`POST /api/v1/study-records`

요청 예시:

```json
{
  "topic": "FastAPI routing",
  "minutes": 45
}
```

- 상태 코드: `201 Created`
- `topic`은 앞뒤 공백을 제거한 뒤 1~100자여야 합니다.
- `minutes`는 1~720 사이의 정수여야 합니다.
- 응답에는 서버가 만든 양의 정수 `id`와 `completed: false`가 포함됩니다.

### 3. 전체 학습 기록 조회

`GET /api/v1/study-records`

- 상태 코드: `200 OK`
- 생성 순서대로 배열을 반환합니다.
- 기록이 없으면 빈 배열을 반환합니다.

### 4. 단일 학습 기록 조회

`GET /api/v1/study-records/{record_id}`

- 존재하면 `200 OK`와 해당 기록을 반환합니다.
- 존재하지 않으면 `404 Not Found`와
  `{"detail": "Study record not found"}`를 반환합니다.

### 5. 학습 완료 처리

`PATCH /api/v1/study-records/{record_id}/complete`

- 존재하면 `completed`를 `true`로 바꾸고 `200 OK`로 반환합니다.
- 여러 번 호출해도 결과는 같습니다.
- 존재하지 않으면 단일 조회와 동일한 `404`를 반환합니다.

## 제약

- 테스트 파일은 수정하지 않습니다.
- 전역 리스트를 라우터에서 직접 조작하지 말고 제공된 `StudyRecordRepository`를
  사용합니다.
- 테스트를 통과시키기 위한 URL별 하드코딩은 금지합니다.
- 새로운 패키지는 필요하지 않습니다.

## 채점

```bash
pytest -q
```

처음에는 실패하는 것이 정상입니다. 테스트 하나씩 통과시키세요. 서버를 직접
확인하려면 다음 명령을 실행하고 `http://127.0.0.1:8000/docs`를 여세요.

```bash
uvicorn app.main:app --reload
```

## 권장 구현 순서

1. `/health`
2. 요청 모델 검증
3. 저장소의 생성·목록 조회
4. 생성·목록 API
5. 단일 조회와 404 처리
6. 완료 처리

## 완료 후 생각해 볼 질문

- 메모리 저장 방식이 실제 서버에서 위험한 이유는 무엇일까요?
- 요청 모델과 응답 모델을 분리하면 어떤 장점이 있을까요?
- `404` 처리를 저장소와 라우터 중 어디서 책임지는 편이 좋을까요?


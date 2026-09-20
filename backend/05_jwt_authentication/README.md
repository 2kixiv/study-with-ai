# 05. JWT 인증과 접근 제어

## 목표

비밀번호를 안전하게 해시해 저장하고, 로그인 성공 시 JWT 액세스 토큰을
발급합니다. 인증된 활성 사용자만 자신의 정보를 조회할 수 있도록 FastAPI
의존성으로 접근 제어를 구현합니다.

```text
가입 → 비밀번호 해시 → PostgreSQL 저장
로그인 → 비밀번호 검증 → JWT 발급
요청 → Bearer 토큰 검증 → 사용자 조회 → 활성 여부 확인 → 엔드포인트
```

## 실행 준비

```bash
cd backend/05_jwt_authentication
docker compose up -d --wait
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
alembic upgrade head
```

## API 요구사항

### 회원 가입

`POST /api/v1/auth/register`

```json
{
  "email": "USER@example.com",
  "name": "Learner",
  "password": "safe-password"
}
```

- 성공: `201 Created`
- 이메일은 검증 후 소문자로 저장합니다.
- 이름은 공백 제거 후 1~50자입니다.
- 비밀번호는 8~128자입니다.
- 비밀번호 원문은 DB와 API 응답 어디에도 저장·노출하지 않습니다.
- 중복 이메일: `409`, `{"detail": "Email already exists"}`

### 로그인

`POST /api/v1/auth/token`

OAuth2 form 형식을 사용합니다. `username` 필드에 이메일을 입력합니다.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=user@example.com&password=safe-password'
```

성공 응답:

```json
{"access_token": "...", "token_type": "bearer"}
```

이메일 또는 비밀번호가 잘못되면 구분하지 않고 `401`과
`{"detail": "Invalid credentials"}`를 반환합니다.

### 현재 사용자

`GET /api/v1/users/me`

```text
Authorization: Bearer <access_token>
```

- 유효한 토큰과 활성 사용자: `200`
- 없거나 변조됐거나 만료된 토큰: `401`
- 비활성 사용자: `403`, `{"detail": "Inactive user"}`

### 계정 비활성화

`POST /api/v1/users/me/deactivate`

- 현재 사용자를 비활성화하고 사용자 정보를 반환합니다.
- 기존 토큰을 다시 사용하면 `403`을 반환합니다.

## JWT 요구사항

- 알고리즘은 설정의 `HS256`을 사용합니다.
- `sub`에는 사용자 ID를 문자열로 저장합니다.
- `iat`와 `exp`를 포함합니다.
- 기본 만료 시간은 설정의 30분입니다.
- 토큰 디코딩 결과에서 `sub`가 없거나 정수가 아니면 인증 실패입니다.

## 파일별 구현 대상

- `schemas.py`: 가입 입력 검증과 이메일 정규화
- `security.py`: 해시·검증, JWT 생성·디코딩
- `repository.py`: 사용자 저장·조회·비활성화, 중복 롤백
- `service.py`: 가입과 로그인 유스케이스
- `dependencies.py`: 토큰으로 현재 사용자 조회, 활성 사용자 확인

ORM 모델과 Alembic 마이그레이션, 라우터, 예외의 HTTP 변환은 제공됩니다.

## 제약

- 테스트를 수정하지 않습니다.
- 비밀번호를 평문으로 저장하거나 응답하지 않습니다.
- 직접 만든 단순 해시 대신 제공된 `PasswordHash`를 사용합니다.
- JWT 서명을 검증하지 않고 payload만 읽지 않습니다.
- 이메일 존재 여부와 비밀번호 오류를 다른 메시지로 응답하지 않습니다.
- 빈 `except:`를 사용하지 않습니다.
- `IntegrityError` 후 반드시 롤백합니다.

## 채점

```bash
pytest -q
```

서버 실행:

```bash
uvicorn app.main:app --reload
```

Swagger UI의 `Authorize`에서 username에는 이메일, password에는 비밀번호를
입력해 인증 흐름을 확인할 수 있습니다.

## 권장 구현 순서

1. `schemas.py`
2. `security.py`의 비밀번호 함수
3. `repository.py`
4. `service.py`
5. `security.py`의 JWT 함수
6. `dependencies.py`
7. 전체 테스트

## 완료 후 생각해 볼 질문

- 비밀번호를 암호화가 아니라 단방향 해시로 저장하는 이유는 무엇일까요?
- 이메일 존재 여부와 비밀번호 오류를 같은 메시지로 처리하는 이유는 무엇일까요?
- JWT를 서버에서 즉시 폐기하기 어려운 이유는 무엇일까요?
- 계정 비활성화 후 기존 토큰을 차단할 수 있는 이유는 무엇일까요?


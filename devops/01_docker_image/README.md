# 01. FastAPI 애플리케이션 컨테이너화

## 목표

제공된 FastAPI 애플리케이션을 운영 가능한 Docker 이미지로 만듭니다.
Dockerfile 명령의 역할, 빌드 컨텍스트, 레이어 캐시, 포트와 바인딩 주소,
비루트 사용자 실행을 익힙니다.

이 과제의 애플리케이션 코드는 완성되어 있습니다. `Dockerfile`과
`.dockerignore`의 `TODO`만 구현하세요.

## 준비

- Docker Engine 또는 Docker Desktop
- Python 3.11 이상(정적 테스트 실행용)

```bash
cd devops/01_docker_image
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

## 문제

다음 조건을 모두 만족하는 컨테이너 이미지를 작성하세요.

### Dockerfile 요구사항

1. 공식 `python:3.12-slim` 이미지를 기반으로 합니다.
2. 컨테이너의 작업 디렉터리는 `/app`입니다.
3. `requirements.txt`를 애플리케이션 코드보다 먼저 복사하고 의존성을
   설치합니다. 코드만 바뀐 빌드에서 의존성 레이어를 재사용하기 위함입니다.
4. pip 캐시를 이미지에 남기지 않도록 `--no-cache-dir` 옵션을 사용합니다.
5. `app` 디렉터리를 이미지의 `/app/app`에 복사합니다.
6. 전용 일반 사용자를 생성하고 그 사용자로 애플리케이션을 실행합니다.
   사용자 이름은 자유지만 `root`로 실행하면 안 됩니다.
7. 이미지가 사용하는 포트 `8000`을 문서화합니다.
8. exec 형식(JSON 배열)의 `CMD`로 아래와 같은 서버를 실행합니다.

```text
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

`127.0.0.1`에 바인딩하면 컨테이너 밖에서 접근할 수 없다는 점에
주의하세요.

### .dockerignore 요구사항

최소한 다음 항목이 빌드 컨텍스트에 들어가지 않게 합니다.

- Git 메타데이터: `.git`
- 가상 환경: `.venv`
- Python 캐시: `__pycache__`, `*.pyc`
- pytest 캐시: `.pytest_cache`
- 과제 테스트: `tests`
- 로컬 환경 파일: `.env`, `.env.*`

## 검증

먼저 빠른 정적 테스트를 실행합니다.

```bash
pytest -q
```

테스트를 통과하면 이미지를 실제로 빌드하고 컨테이너를 실행합니다.

```bash
docker build -t study-api:01 .
docker run --rm -p 8000:8000 study-api:01
```

다른 터미널에서 다음 응답을 확인합니다.

```bash
curl http://127.0.0.1:8000/health
# {"status":"ok"}
```

실행 중인 사용자가 root가 아닌지도 확인하세요.

```bash
docker run --rm study-api:01 id -u
# 0이 아닌 값
```

## 제약

- `app`, `tests`, `requirements.txt`, `requirements-dev.txt`는 수정하지 않습니다.
- 애플리케이션 소스나 테스트를 이미지에 맞춰 변경하지 않습니다.
- 컨테이너를 `root` 사용자로 실행하지 않습니다.
- 비밀값이나 로컬 환경 파일을 이미지에 복사하지 않습니다.
- `CMD`에 shell 형식 문자열을 사용하지 않습니다.

## 권장 구현 순서

1. 베이스 이미지와 작업 디렉터리 지정
2. 의존성 파일 복사와 설치
3. 애플리케이션 코드 복사
4. 일반 사용자 생성과 전환
5. 포트와 실행 명령 설정
6. `.dockerignore` 작성
7. 정적 테스트 후 실제 빌드·실행

## 완료 후 생각해 볼 질문

- `COPY . .`보다 필요한 파일만 복사하는 방식은 어떤 장점이 있을까요?
- 의존성 파일을 코드보다 먼저 복사하면 빌드 시간이 줄어드는 이유는
  무엇일까요?
- `EXPOSE 8000`과 `docker run -p 8000:8000`은 각각 무엇을 할까요?
- 컨테이너 프로세스를 비루트 사용자로 실행해야 하는 이유는 무엇일까요?

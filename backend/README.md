# Backend 문제 풀이 트랙

HTTP와 FastAPI 기초에서 출발해 데이터베이스, 보안, 비동기 처리, 관측 가능성,
분산 시스템까지 단계적으로 학습합니다. 과제 수는 고정하지 않으며 필요하면
각 단계 사이에 보충 과제를 추가합니다.

## 학습 방식

1. 과제 폴더의 `README.md`만 먼저 읽습니다.
2. `rg TODO`로 구현 위치를 확인합니다.
3. 테스트 이름과 실패 메시지로 필요한 동작을 추론합니다.
4. 단위 테스트, 통합 테스트, 실제 서버 실행 순서로 검증합니다.
5. 완료 후 HTTP·데이터·동시성·보안 관점에서 다시 검토합니다.

## 1단계: 웹 API와 데이터베이스 기초

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 01 | FastAPI 첫 CRUD | HTTP 메서드, 경로, 상태 코드, Pydantic 검증 |
| 02 | 계층형 아키텍처 | router/service/repository, 의존성 주입 |
| 03 | PostgreSQL 연결 | Docker Compose, SQLAlchemy 세션, 영속성 |
| 04 | 사용자 CRUD와 마이그레이션 | Alembic, 유일성, 스키마 변경 |
| 05 | JWT 인증 | 비밀번호 해시, access token, 인증 의존성 |
| 06 | 게시글과 관계 | 외래 키, 소유권, 검색, 페이지네이션, N+1 |
| 07 | 테스트 가능한 DB 설계 | fixture, 테스트 DB, 트랜잭션 격리 |
| 08 | 트랜잭션과 동시성 | 원자성, 격리 수준, 행 잠금, 재고 차감 |
| 09 | 운영 설정과 상태 확인 | 환경별 설정, 구조화 로그, health/readiness |

## 2단계: 실무 API 기능

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 10 | Redis 캐시 | cache-aside, TTL, 무효화, cache stampede |
| 11 | 요청 제한 | rate limit, sliding window, 사용자·IP 기준 |
| 12 | 백그라운드 작업 | 요청 생명주기, 재시도, 실패 기록 |
| 13 | 작업 큐 | producer/consumer, Celery 또는 RQ, 멱등성 |
| 14 | 파일 업로드 | 스트리밍, 크기·형식 검증, 객체 저장소 |
| 15 | 이메일과 웹훅 | 외부 통신, 서명 검증, 재시도와 중복 방지 |
| 16 | WebSocket | 연결 관리, 브로드캐스트, 재연결 |
| 17 | 전문 검색 | PostgreSQL FTS, 인덱스, 검색 랭킹 |
| 18 | 비동기 DB 접근 | async/await, async session, 동시성 한계 |

## 3단계: 품질, 보안, 성능

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 19 | 테스트 전략 | 단위·통합·E2E, test double, 실패 격리 |
| 20 | 계약 테스트 | OpenAPI 계약, 호환성, consumer 관점 테스트 |
| 21 | 쿼리 최적화 | 실행 계획, 인덱스, slow query, N+1 진단 |
| 22 | 애플리케이션 프로파일링 | CPU·메모리·I/O 병목 측정 |
| 23 | 부하 테스트 | 처리량, latency percentile, 포화 지점 |
| 24 | API 보안 기초 | OWASP API Top 10, 입력 공격, CORS, CSRF |
| 25 | 인증 심화 | refresh token, token rotation, 세션 폐기 |
| 26 | 권한 모델 | RBAC, ABAC, 리소스 단위 권한 |
| 27 | 관측 가능성 | 로그, 메트릭, trace, correlation ID |
| 28 | API 버전과 호환성 | 버전 정책, deprecation, 점진적 변경 |

## 4단계: 아키텍처와 분산 시스템

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 29 | 모듈러 모놀리스 | bounded module, 내부 API, 의존성 방향 |
| 30 | 도메인 모델링 | entity, value object, aggregate, 도메인 규칙 |
| 31 | 이벤트와 Outbox | 트랜잭션 이벤트, outbox relay, 중복 소비 |
| 32 | 마이크로서비스 분리 | 서비스 경계, 데이터 소유권, 계약 |
| 33 | gRPC 서비스 | protobuf, unary/streaming, deadline |
| 34 | 메시지 브로커 | Kafka/RabbitMQ, partition, ordering, ack |
| 35 | 이벤트 기반 처리 | consumer group, 재처리, dead-letter queue |
| 36 | 분산 트랜잭션 | Saga, 보상 작업, 최종 일관성 |
| 37 | 복원력 패턴 | timeout, retry, backoff, circuit breaker |
| 38 | 분산 캐시와 잠금 | 일관성, fencing token, lock 만료 |
| 39 | 서비스 간 인증 | service identity, mTLS, 최소 권한 |

## 5단계: 고급 운영 프로젝트

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 40 | 멀티테넌시 | tenant 격리, 쿼리 필터, 데이터 전략 |
| 41 | 감사 로그 | 변경 이력, 불변성, 개인정보 마스킹 |
| 42 | Feature Flag | 점진적 공개, kill switch, 실험 분기 |
| 43 | 결제 흐름 | 멱등 키, 상태 머신, 웹훅 정합성 |
| 44 | 알림 시스템 | fan-out, 사용자 설정, 전달 보장 |
| 45 | 종합 서비스 | 설계·구현·부하·보안·운영 검증 |

45번 이후에는 GraphQL, CDC, CQRS, 대규모 검색, 지리 분산, 데이터 보존 정책
등을 학습 목표에 맞춰 계속 확장합니다.

## 공통 원칙

- Python 3.11 이상을 사용합니다.
- API 오류는 의미 있는 상태 코드와 안정적인 응답 계약으로 표현합니다.
- 저장소와 서비스 계층에 HTTP 세부 구현을 무분별하게 섞지 않습니다.
- 데이터 정합성은 애플리케이션과 데이터베이스 제약을 함께 사용해 지킵니다.
- 테스트 통과뿐 아니라 타입, 이름, 로그가 의도를 드러내야 합니다.
- 과제 폴더끼리 코드를 import하지 않습니다.


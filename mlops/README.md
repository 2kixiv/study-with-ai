# MLOps 문제 풀이 트랙

모델 실험 한 번을 기록하는 것에서 시작해 데이터·모델 버전, 학습 파이프라인,
검증과 승인, 배포, 모니터링, 재학습, 거버넌스까지 전체 모델 수명주기를
단계적으로 학습합니다. 과제 수는 고정하지 않고 새로운 운영 문제와 도구를
계속 반영합니다.

## 선수 학습

- `ml-engineering/machine-learning`에서 최소 하나의 회귀 또는 분류 모델 완성
- 재현 가능한 train/validation/test 분할과 평가 지표 이해
- `devops`의 Docker와 기본 CI 개념 이해

첫 과제는 독립적으로 실행할 수 있도록 작은 학습 코드를 제공합니다.

## 학습 방식

1. 과제 README에서 추적하거나 자동화할 수명주기 단계를 확인합니다.
2. 로컬 환경에서 가장 작은 구성으로 동작을 검증합니다.
3. 데이터, 코드, 설정, 모델, 실행 결과 사이의 연결을 기록합니다.
4. 성공 경로뿐 아니라 실패, 재시도, 승인 거부, 롤백을 테스트합니다.
5. 이후 과제에서 원격 저장소와 자동화 환경으로 확장합니다.

## 1단계: 재현성과 실험 관리

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 01 | MLflow 실험 추적 | parameter, metric, tag, signature, model artifact |
| 02 | 실행 설정 관리 | config file, environment override, 설정 snapshot |
| 03 | 재현 가능한 학습 | seed, dependency lock, environment, code version |
| 04 | 아티팩트 관리 | 경로, checksum, metadata, retention |
| 05 | 실험 비교 | 기준 run, metric 비교, query, visualization |
| 06 | 모델 카드 | 목적, 데이터, 지표, 한계, 책임 정보 |

## 2단계: 데이터와 모델 버전 관리

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 07 | 데이터 버전 관리 | DVC, remote, hash, checkout |
| 08 | 데이터 계보 | raw/processed/features/model 관계 |
| 09 | 데이터 품질 게이트 | schema, statistics, drift 전 검사 |
| 10 | 학습 데이터 snapshot | query/version/time 기준 재현 |
| 11 | 모델 패키지 버전 | model, preprocessor, signature, dependency |
| 12 | 모델 레지스트리 기초 | version, stage/alias, metadata |
| 13 | 모델 승인 흐름 | candidate 비교, reviewer, promotion condition |
| 14 | 모델 롤백 | 이전 alias 복원, 호환성, rollback test |

## 3단계: 학습 파이프라인

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 15 | 파이프라인 단계 분리 | ingest/validate/train/evaluate/package |
| 16 | DAG와 의존성 | task input/output, ordering, visualization |
| 17 | 캐시와 증분 실행 | artifact fingerprint, 변경 단계만 재실행 |
| 18 | 재시도와 실패 복구 | retryable error, timeout, checkpoint |
| 19 | backfill과 재학습 | 기준 시점, 범위 실행, 중복 방지 |
| 20 | 파이프라인 테스트 | unit, component, integration, smoke test |
| 21 | 로컬 오케스트레이션 | Prefect/Airflow 기본 flow와 상태 |
| 22 | 원격 실행 | worker, queue, artifact store, secret |
| 23 | 정기·이벤트 트리거 | schedule, 새 데이터, 수동 승인 |

## 4단계: ML CI와 품질 게이트

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 24 | ML 코드 CI | lint, unit test, type check, 작은 학습 |
| 25 | 데이터 CI | schema·quality 검사, fixture, sample data |
| 26 | 모델 회귀 테스트 | golden set, metric tolerance, behavior test |
| 27 | 편향과 공정성 검사 | slice metric, disparity, 승인 기준 |
| 28 | 보안 검사 | dependency, unsafe serialization, secret scan |
| 29 | 학습 이미지 빌드 | reproducible image, cache, CPU/GPU variant |
| 30 | 파이프라인 CI | artifact 전달, 조건부 실행, 실패 보고 |
| 31 | 자동 승격 게이트 | 기준 모델 대비 품질·성능 조건 |

## 5단계: 서빙과 배포

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 32 | 배치 모델 배포 | schedule, input/output version, partial retry |
| 33 | 온라인 모델 배포 | model server, readiness, signature validation |
| 34 | Registry 기반 로딩 | alias, startup load, cache, fallback |
| 35 | 환경별 배포 | development/staging/production, 승인 |
| 36 | Shadow 배포 | 운영 요청 복제, 응답 비교, 사용자 영향 제거 |
| 37 | Canary 배포 | traffic split, success metric, 자동 중단 |
| 38 | A/B 테스트 | 실험 단위, assignment, guardrail metric |
| 39 | 모델 롤백 자동화 | 실패 조건, alias 복원, 사후 검증 |
| 40 | GPU 모델 배포 | device scheduling, batching, warm-up |

## 6단계: 모델 관측과 재학습

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 41 | 추론 로그 설계 | request ID, model version, privacy, sampling |
| 42 | 서비스 메트릭 | latency, traffic, error, saturation |
| 43 | 입력 데이터 품질 | missing, range, category, schema change |
| 44 | 데이터 drift | reference/current, PSI, KS, distribution shift |
| 45 | prediction drift | score·class 분포, segment별 변화 |
| 46 | 실제 성능 추적 | 지연 label, join, rolling metric |
| 47 | 모델별 대시보드 | 서비스·데이터·모델 지표 연결 |
| 48 | 모델 알림 | threshold, window, minimum sample, noise 억제 |
| 49 | 재학습 트리거 | schedule/drift/performance/manual 조건 |
| 50 | 자동 재학습 | 새 snapshot, validation, candidate 생성 |
| 51 | 인간 승인 단계 | review, evidence, audit trail |
| 52 | 폐쇄 루프 검증 | 재학습 후 배포·모니터링·롤백 |

## 7단계: 확장, 거버넌스, 플랫폼

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 53 | Feature Store 운영 | offline/online sync, freshness, ownership |
| 54 | 다중 모델 관리 | tenant/model routing, resource isolation |
| 55 | 분산 학습 운영 | job scheduling, checkpoint, preemption |
| 56 | 비용 추적 | run/model/team 비용, GPU utilization |
| 57 | 데이터·모델 접근 제어 | identity, role, least privilege |
| 58 | 감사와 규정 준수 | lineage, approval, retention, deletion |
| 59 | 개인정보 보호 | masking, minimization, deletion propagation |
| 60 | MLOps 플랫폼 API | self-service template, golden path |
| 61 | 다중 환경·클러스터 | promotion, artifact replication, disaster recovery |
| 62 | 종합 운영 프로젝트 | 데이터부터 재학습까지 전체 수명주기 |

62번 이후에는 LLMOps, prompt/version/evaluation, RAG 관측, online learning,
federated learning, 대규모 GPU 스케줄링 등을 별도 심화 과정으로 확장합니다.

## 다른 트랙과의 경계

| 트랙 | 주된 책임 |
|---|---|
| ML Engineering | 데이터·모델·학습·추론 코드 자체의 정확성과 성능 |
| MLOps | 실행 추적, 버전, 자동화, 승인, 배포, 모니터링 |
| DevOps | 공통 인프라, 컨테이너, CI/CD, Kubernetes, 신뢰성 기반 |

같은 주제를 다른 관점에서 반복할 수 있습니다. 예를 들어 모델 서빙은 ML
Systems에서는 batching과 추론 성능을, MLOps에서는 버전 승격과 안전한 배포를,
DevOps에서는 컨테이너와 Kubernetes 운영을 중심으로 다룹니다.

## 공통 원칙

- 파라미터, 데이터, 코드, 환경, 모델, 지표를 하나의 실행으로 추적합니다.
- 비밀값과 원본 개인정보를 실험 기록이나 아티팩트에 넣지 않습니다.
- 운영 승격은 명시적인 품질 조건과 감사 가능한 근거를 가져야 합니다.
- 자동화에는 중복 실행, 부분 실패, 재시도, 롤백 설계가 포함되어야 합니다.
- 과제 폴더끼리 코드를 직접 import하지 않습니다.


# DevOps 문제 풀이 트랙

작은 애플리케이션 컨테이너에서 시작해 Linux, 네트워크, CI/CD, Kubernetes,
인프라 코드, 관측 가능성과 SRE까지 확장합니다. 도구 사용법만 외우지 않고
프로세스·네트워크·권한·장애 복구 원리를 함께 학습합니다.

첫 Docker 과제는 빠르게 실행 결과를 만드는 입문 과제입니다. 이후 Linux와
네트워크 기초를 자세히 다룬 뒤 컨테이너 운영으로 돌아옵니다.

## 학습 방식

1. 과제 README의 개념과 운영 시나리오를 읽습니다.
2. `rg TODO`로 구현할 설정과 스크립트를 찾습니다.
3. 정적 검사 후 실제 프로세스나 서비스를 실행합니다.
4. 정상 상태뿐 아니라 종료, 재시작, 장애, 롤백을 검증합니다.
5. 보안, 재현성, 관찰 가능성, 복구 가능성을 함께 평가합니다.

## 1단계: 입문과 Linux 기초

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 01 | 애플리케이션 컨테이너화 | Dockerfile, 레이어, 비루트 사용자, 포트 |
| 02 | Linux 파일 시스템 | 경로, 파일 탐색, 링크, inode, 표준 디렉터리 |
| 03 | 사용자와 권한 | user/group, chmod, umask, sudo, 최소 권한 |
| 04 | 프로세스와 시그널 | PID, foreground/background, signal, graceful shutdown |
| 05 | 셸과 파이프 | stdin/out/err, pipe, redirect, exit code |
| 06 | 안전한 셸 스크립트 | 변수, 조건, 반복, 함수, trap, `set -euo pipefail` |
| 07 | 서비스 관리 | 환경 변수, systemd unit, restart, journal |
| 08 | 디스크와 메모리 | filesystem, mount, swap, memory pressure |

## 2단계: 네트워크와 컨테이너

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 09 | TCP/IP 기초 | IP, subnet, port, socket, 연결 상태 |
| 10 | DNS와 HTTP | 이름 해석, record, HTTP 흐름, timeout |
| 11 | TLS 기초 | 인증서, CA, handshake, 만료 확인 |
| 12 | Docker 이미지 심화 | build context, cache, multi-stage, BuildKit |
| 13 | 컨테이너 런타임 | namespace, cgroup, PID 1, resource limit |
| 14 | 볼륨과 데이터 | bind mount, named volume, 권한, 백업 |
| 15 | 컨테이너 네트워크 | bridge, DNS, port publishing, 격리 |
| 16 | Docker Compose | 다중 서비스, dependency, healthcheck, profile |
| 17 | 이미지 보안 | digest, SBOM, 취약점, secret mount |
| 18 | 리버스 프록시 | Nginx 라우팅, header, timeout, 정적 파일 |
| 19 | HTTPS 운영 | 인증서 자동 갱신, redirect, 보안 헤더 |

## 3단계: CI/CD와 릴리스

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 20 | CI 첫 파이프라인 | checkout, lint, test, 실패 처리 |
| 21 | CI 의존성과 캐시 | lock file, cache key, 재현 가능한 빌드 |
| 22 | 병렬 작업과 아티팩트 | matrix, job dependency, artifact 전달 |
| 23 | 컨테이너 레지스트리 | tag, digest, immutable release, 정리 정책 |
| 24 | 공급망 보안 | dependency scan, image scan, SBOM, 서명 |
| 25 | 환경과 비밀 관리 | dev/stage/prod, secret 주입, rotation |
| 26 | CD 기본 배포 | 승인, migration 순서, smoke test |
| 27 | 무중단 배포 | rolling, blue-green, canary |
| 28 | 롤백과 복구 | 실패 감지, 자동 중단, 이전 버전 복원 |

## 4단계: Kubernetes

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 29 | Pod와 컨테이너 | Pod 수명주기, 로그, exec, restart policy |
| 30 | Deployment와 Service | replica, rollout, ClusterIP, DNS |
| 31 | 설정과 비밀 | ConfigMap, Secret, volume, 갱신 전략 |
| 32 | Probe와 종료 | startup/readiness/liveness, preStop, grace period |
| 33 | 리소스 관리 | request/limit, QoS, OOM, scheduling |
| 34 | 저장소 | PV, PVC, StorageClass, StatefulSet |
| 35 | Ingress와 TLS | ingress controller, host routing, 인증서 |
| 36 | Job과 CronJob | 일회성 작업, 재시도, 동시 실행 정책 |
| 37 | 권한과 보안 | namespace, ServiceAccount, RBAC, security context |
| 38 | 오토스케일링 | HPA, metric, capacity, cluster autoscaling |
| 39 | 패키지 관리 | Helm chart, values, template, release |
| 40 | 장애 진단 | event, log, metric, pending/crash/network 문제 |

## 5단계: Infrastructure as Code와 구성 관리

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 41 | Terraform 기초 | provider, resource, plan, apply, dependency |
| 42 | Terraform 상태 | remote state, lock, import, drift |
| 43 | 모듈과 환경 | input/output, module, workspace 전략 |
| 44 | 네트워크 인프라 | VPC, subnet, route, firewall, load balancer |
| 45 | 컴퓨팅과 관리형 서비스 | VM, container service, database, IAM |
| 46 | IaC 테스트와 정책 | format, validate, plan review, policy as code |
| 47 | Ansible 기초 | inventory, playbook, idempotency, handler |
| 48 | 서버 구성 자동화 | 패키지, 사용자, 서비스, 보안 설정 |

## 6단계: 관측 가능성과 SRE

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 49 | 구조화 로그 | 수집, 필드, 검색, 보존, 민감정보 제거 |
| 50 | 메트릭 | counter/gauge/histogram, Prometheus scrape |
| 51 | 대시보드 | RED/USE method, Grafana, 유용한 시각화 |
| 52 | 분산 추적 | trace/span, context propagation, sampling |
| 53 | 알림 설계 | 증상 기반 알림, noise, routing, escalation |
| 54 | SLI·SLO·Error Budget | 신뢰성 목표, burn rate, 출시 판단 |
| 55 | 용량 계획 | 부하 모델, 병목, headroom, 비용 |
| 56 | 백업과 복구 | RPO/RTO, restore drill, 재해 복구 |
| 57 | 장애 대응 | incident role, runbook, communication |
| 58 | 포스트모템 | timeline, 근본 원인, 재발 방지 |
| 59 | 비용 최적화 | 사용량, right-sizing, idle resource, 예산 알림 |
| 60 | 운영 종합 프로젝트 | 배포·관측·보안·장애 훈련 통합 |

60번 이후에는 GitOps, service mesh, multi-cluster, chaos engineering, 플랫폼
엔지니어링, 정책 관리 등을 필요에 따라 계속 추가합니다.

## 공통 원칙

- 모든 변경은 다시 만들 수 있고 검토 가능한 형태로 남깁니다.
- 비밀값을 저장소, 이미지, 로그, Terraform state에 노출하지 않습니다.
- root와 과도한 권한을 피하고 최소 권한을 적용합니다.
- 자동화 성공뿐 아니라 실패·중단·롤백 경로도 테스트합니다.
- 운영 절차는 사람의 기억이 아니라 코드와 문서에 남깁니다.
- 과제 폴더끼리 파일을 직접 참조하지 않습니다.


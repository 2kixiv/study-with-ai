# 01. MLflow 실험 추적

## 목표

작은 회귀 모델의 학습 실행을 MLflow에 기록합니다. 파라미터, 평가 지표,
태그, 모델 아티팩트를 하나의 run으로 묶고 추적 저장소에서 다시 조회할 수
있게 만듭니다.

모델 학습용 데이터 생성 코드는 제공됩니다. `src/train.py`의 `TODO`를 구현해
실험 추적에 집중하세요.

## 준비

```bash
cd mlops/01_experiment_tracking
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 문제

`train_and_track()`이 다음 작업을 수행하게 구현하세요.

1. 인자로 받은 `tracking_uri`를 MLflow에 설정합니다.
2. 인자로 받은 이름의 실험을 생성하거나 기존 실험을 사용합니다.
3. 하나의 MLflow run 안에서 `Ridge` 모델을 학습합니다.
4. 다음 파라미터를 기록합니다.
   - `model_type`: `Ridge`
   - `alpha`: 함수 인자값
   - `random_state`: 함수 인자값
5. test set에서 `mse`와 `r2`를 계산해 지표로 기록합니다.
6. 다음 태그를 기록합니다.
   - `project`: `study-with-ai`
   - `pipeline_stage`: `training`
7. signature와 input example을 포함한 sklearn 모델을 `model` 경로에 기록합니다.
8. run ID와 계산한 지표가 담긴 `TrainingResult`를 반환합니다.

같은 `random_state`로 데이터 생성과 train/test 분할을 수행해야 합니다.

## 실행과 채점

```bash
pytest -q
```

직접 실행한 뒤 MLflow UI에서 기록을 살펴볼 수도 있습니다.

```bash
python -m src.train
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

브라우저에서 `http://127.0.0.1:5000`을 엽니다.

## 제약

- 테스트를 수정하지 않습니다.
- 전역 autolog 기능에 의존하지 않고 요구된 값을 명시적으로 기록합니다.
- 학습 데이터나 개인정보를 파라미터·태그에 기록하지 않습니다.
- test set으로 모델을 학습하지 않습니다.
- run이 종료된 뒤에도 모델을 추적 저장소에서 로드할 수 있어야 합니다.

## 권장 구현 순서

1. tracking URI와 실험 설정
2. run 컨텍스트 시작
3. 데이터 분할과 모델 학습
4. 지표 계산 및 파라미터·지표·태그 기록
5. signature 추론과 모델 기록
6. 결과 객체 반환 후 테스트

## 완료 후 생각해 볼 질문

- 모델 파일만 저장하는 것보다 run으로 기록하는 방식은 어떤 장점이 있을까요?
- 파라미터와 태그는 어떻게 다르게 사용해야 할까요?
- 동일한 난수 시드를 기록했는데도 결과가 달라질 수 있는 이유는 무엇일까요?
- 운영 모델로 승격하기 전에 어떤 지표와 조건을 추가로 검사해야 할까요?

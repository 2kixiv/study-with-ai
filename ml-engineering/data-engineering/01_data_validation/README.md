# 01. 데이터 검증과 재현 가능한 분할

## 목표

CSV 데이터를 DataFrame으로 읽고 명시적인 데이터 계약을 검증합니다. 모델
학습 전에 잘못된 데이터를 빠르게 차단하고, 식별자·정답 열의 누수 없이
재현 가능한 stratified train/test split을 만듭니다.

## 준비

```bash
cd ml-engineering/data-engineering/01_data_validation
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 문제

`src/data_pipeline.py`의 `TODO`를 구현하세요.

### 데이터 계약

입력 CSV에는 다음 열이 모두 있어야 합니다. 추가 열은 허용합니다.

| 열 | 의미 | 조건 |
|---|---|---|
| `learner_id` | 학습자 식별자 | 결측값·중복 없음 |
| `age` | 나이 | 정수, 10~100 |
| `study_hours` | 하루 학습 시간 | 숫자, 0~24 |
| `attendance_rate` | 출석률 | 숫자, 0~1 |
| `previous_score` | 이전 점수 | 숫자, 0~100 |
| `passed` | 합격 여부 | 정수 `0` 또는 `1` |

필수 열의 결측값, 잘못된 범위, 잘못된 정답값을 발견하면 제공된
`DataValidationError`를 발생시키세요. 오류 메시지는 문제의 원인을 식별할 수
있어야 합니다.

### 분할 계약

`prepare_dataset()`은 다음 조건을 만족하는 `DatasetSplit`을 반환합니다.

- `passed`를 정답(`y`)으로 분리합니다.
- `learner_id`와 `passed`는 특성(`X`)에 포함하지 않습니다.
- `train_test_split()`에 `stratify=y`를 적용합니다.
- 전달받은 `test_size`와 `random_state`를 사용합니다.
- 같은 입력과 시드로 실행하면 같은 행이 나뉩니다.
- train과 test의 원본 인덱스는 서로 겹치지 않습니다.

## 제약

- 테스트와 예제 CSV를 수정하지 않습니다.
- 유효하지 않은 행을 조용히 삭제하거나 값을 임의로 보정하지 않습니다.
- 분할 전에 전체 데이터로 전처리나 모델 학습을 수행하지 않습니다.
- `learner_id`를 모델 특성으로 사용하지 않습니다.

## 실행과 채점

```bash
pytest -q
```

## 권장 구현 순서

1. CSV 로딩과 필수 열 검사
2. 결측값과 식별자 중복 검사
3. 각 열의 타입·범위 검사
4. 특성과 정답 분리
5. stratified split과 결과 객체 생성

## 완료 후 생각해 볼 질문

- 잘못된 행을 삭제하지 않고 실패시키는 것이 안전한 이유는 무엇일까요?
- 식별자가 높은 예측력을 보이더라도 특성에서 제외해야 하는 이유는 무엇일까요?
- 일반 무작위 분할 대신 stratified split이 필요한 경우는 언제일까요?
- 난수 시드만 같으면 모든 환경에서 완전히 같은 결과를 보장할 수 있을까요?

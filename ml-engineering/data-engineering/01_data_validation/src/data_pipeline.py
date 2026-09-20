from dataclasses import dataclass
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = (
    "learner_id",
    "age",
    "study_hours",
    "attendance_rate",
    "previous_score",
    "passed",
)


class DataValidationError(ValueError):
    """입력 데이터가 학습 데이터 계약을 위반했을 때 발생합니다."""


@dataclass(frozen=True)
class DatasetSplit:
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series


def load_and_validate(path: str | Path) -> pd.DataFrame:
    """CSV를 읽어 데이터 계약을 검증한 뒤 반환합니다."""
    # TODO: CSV 로딩과 필수 열, 결측값, 중복, 타입, 범위를 검증하세요.
    raise NotImplementedError


def prepare_dataset(
    path: str | Path,
    *,
    test_size: float = 0.2,
    random_state: int = 42,
) -> DatasetSplit:
    """검증된 데이터를 누수 없이 재현 가능하게 분할합니다."""
    # TODO: 식별자와 정답 열을 분리하고 stratified split을 수행하세요.
    raise NotImplementedError

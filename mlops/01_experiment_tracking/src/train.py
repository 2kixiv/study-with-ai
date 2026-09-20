from dataclasses import dataclass
from pathlib import Path

import mlflow
import numpy as np
from sklearn.datasets import make_regression


@dataclass(frozen=True)
class TrainingResult:
    run_id: str
    mse: float
    r2: float


def create_dataset(random_state: int) -> tuple[np.ndarray, np.ndarray]:
    """과제에서 사용할 결정론적인 회귀 데이터를 만듭니다."""
    return make_regression(
        n_samples=200,
        n_features=5,
        n_informative=4,
        noise=8.0,
        random_state=random_state,
    )


def train_and_track(
    tracking_uri: str,
    *,
    experiment_name: str = "study-duration",
    alpha: float = 1.0,
    random_state: int = 42,
) -> TrainingResult:
    """Ridge 모델을 학습하고 하나의 MLflow run에 결과를 기록합니다."""
    # TODO: 실험 설정, 학습, 평가, 기록, 모델 저장을 구현하세요.
    raise NotImplementedError


if __name__ == "__main__":
    database_path = (Path.cwd() / "mlflow.db").resolve()
    local_store = f"sqlite:///{database_path}"
    result = train_and_track(local_store)
    print(f"run_id={result.run_id} mse={result.mse:.4f} r2={result.r2:.4f}")

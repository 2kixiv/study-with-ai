from pathlib import Path

import mlflow
import mlflow.sklearn
import pytest

from src.train import TrainingResult, train_and_track


@pytest.fixture
def tracking_uri(tmp_path: Path) -> str:
    database_path = (tmp_path / "mlflow.db").resolve()
    return f"sqlite:///{database_path}"


def run_training(tracking_uri: str) -> TrainingResult:
    return train_and_track(
        tracking_uri,
        experiment_name="assignment-test",
        alpha=0.75,
        random_state=17,
    )


def test_returns_finished_run_with_metrics(tracking_uri: str) -> None:
    result = run_training(tracking_uri)
    run = mlflow.MlflowClient(tracking_uri=tracking_uri).get_run(result.run_id)

    assert run.info.status == "FINISHED"
    assert result.mse >= 0
    assert -1 <= result.r2 <= 1
    assert run.data.metrics["mse"] == pytest.approx(result.mse)
    assert run.data.metrics["r2"] == pytest.approx(result.r2)


def test_logs_required_parameters_and_tags(tracking_uri: str) -> None:
    result = run_training(tracking_uri)
    run = mlflow.MlflowClient(tracking_uri=tracking_uri).get_run(result.run_id)

    assert run.data.params == {
        "model_type": "Ridge",
        "alpha": "0.75",
        "random_state": "17",
    }
    assert run.data.tags["project"] == "study-with-ai"
    assert run.data.tags["pipeline_stage"] == "training"


def test_logs_loadable_model_with_signature(tracking_uri: str) -> None:
    result = run_training(tracking_uri)
    client = mlflow.MlflowClient(tracking_uri=tracking_uri)
    artifacts = client.list_artifacts(result.run_id, "model")

    assert artifacts, "model 경로에 sklearn 모델을 기록하세요."

    model_uri = f"runs:/{result.run_id}/model"
    model = mlflow.sklearn.load_model(model_uri)
    model_info = mlflow.models.get_model_info(model_uri)

    assert model.__class__.__name__ == "Ridge"
    assert model_info.signature is not None
    assert model.predict([[1.0, 2.0, 3.0, 4.0, 5.0]]).shape == (1,)


def test_same_seed_produces_same_metrics(tracking_uri: str) -> None:
    first = run_training(tracking_uri)
    second = run_training(tracking_uri)

    assert first.run_id != second.run_id
    assert first.mse == pytest.approx(second.mse)
    assert first.r2 == pytest.approx(second.r2)

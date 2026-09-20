from pathlib import Path

import pandas as pd
import pytest

from src.data_pipeline import (
    REQUIRED_COLUMNS,
    DataValidationError,
    load_and_validate,
    prepare_dataset,
)


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "study_outcomes.csv"


def write_csv(tmp_path: Path, frame: pd.DataFrame) -> Path:
    path = tmp_path / "input.csv"
    frame.to_csv(path, index=False)
    return path


def valid_frame() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def test_loads_valid_csv() -> None:
    frame = load_and_validate(DATA_PATH)

    assert tuple(frame.columns[: len(REQUIRED_COLUMNS)]) == REQUIRED_COLUMNS
    assert len(frame) == 20


def test_rejects_missing_required_column(tmp_path: Path) -> None:
    path = write_csv(tmp_path, valid_frame().drop(columns="age"))

    with pytest.raises(DataValidationError, match="age"):
        load_and_validate(path)


@pytest.mark.parametrize("column", REQUIRED_COLUMNS)
def test_rejects_null_in_required_column(tmp_path: Path, column: str) -> None:
    frame = valid_frame()
    frame.loc[0, column] = None

    with pytest.raises(DataValidationError, match=column):
        load_and_validate(write_csv(tmp_path, frame))


def test_rejects_duplicate_learner_id(tmp_path: Path) -> None:
    frame = valid_frame()
    frame.loc[1, "learner_id"] = frame.loc[0, "learner_id"]

    with pytest.raises(DataValidationError, match="learner_id"):
        load_and_validate(write_csv(tmp_path, frame))


@pytest.mark.parametrize(
    ("column", "bad_value"),
    [
        ("age", 9),
        ("age", 101),
        ("age", 20.5),
        ("study_hours", -0.1),
        ("study_hours", 24.1),
        ("attendance_rate", -0.1),
        ("attendance_rate", 1.1),
        ("previous_score", -1),
        ("previous_score", 101),
        ("passed", 2),
    ],
)
def test_rejects_invalid_values(
    tmp_path: Path, column: str, bad_value: float
) -> None:
    frame = valid_frame()
    frame[column] = frame[column].astype(float)
    frame.loc[0, column] = bad_value

    with pytest.raises(DataValidationError, match=column):
        load_and_validate(write_csv(tmp_path, frame))


def test_split_excludes_identifier_and_target() -> None:
    split = prepare_dataset(DATA_PATH, test_size=0.2, random_state=7)

    assert list(split.X_train.columns) == [
        "age",
        "study_hours",
        "attendance_rate",
        "previous_score",
    ]
    assert list(split.X_test.columns) == list(split.X_train.columns)
    assert len(split.X_train) == 16
    assert len(split.X_test) == 4


def test_split_is_stratified_and_disjoint() -> None:
    split = prepare_dataset(DATA_PATH, test_size=0.2, random_state=7)

    assert split.y_train.value_counts().to_dict() == {0: 8, 1: 8}
    assert split.y_test.value_counts().to_dict() == {0: 2, 1: 2}
    assert set(split.X_train.index).isdisjoint(split.X_test.index)


def test_split_is_reproducible() -> None:
    first = prepare_dataset(DATA_PATH, test_size=0.2, random_state=17)
    second = prepare_dataset(DATA_PATH, test_size=0.2, random_state=17)

    pd.testing.assert_frame_equal(first.X_train, second.X_train)
    pd.testing.assert_frame_equal(first.X_test, second.X_test)
    pd.testing.assert_series_equal(first.y_train, second.y_train)
    pd.testing.assert_series_equal(first.y_test, second.y_test)

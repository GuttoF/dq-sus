from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from pathlib import Path
from dq_sus.infer_schema.infer_schema import (
    extract_to_infer_schema,
    infer_and_save_schema,
)


@pytest.fixture

def mock_raw_data_path(tmp_path: Path) -> Path:
    return Path(tmp_path) / "raw_data"


@pytest.fixture
def mock_schema_path(tmp_path: Path) -> Path:
    return Path(tmp_path) / "schema"


@pytest.fixture
def mock_data() -> pd.DataFrame:
    return pd.DataFrame({"column1": [1, 2], "column2": ["a", "b"]})


def test_extract_to_infer_schema_file_exists(
    mock_raw_data_path: Path, mock_data: pd.DataFrame
) -> None:
    file_path = mock_raw_data_path / "CHIKBR23.parquet"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    mock_data.to_parquet(file_path)

    with patch("dq_sus.infer_schema.infer_schema.pd.read_parquet") as mock_read_parquet:
        mock_read_parquet.return_value = mock_data
        data = extract_to_infer_schema("CHIK", 2023, mock_raw_data_path)
        mock_read_parquet.assert_called_once_with(file_path)
        pd.testing.assert_frame_equal(data, mock_data)


def test_extract_to_infer_schema_download(
    mock_raw_data_path: Path, mock_data: pd.DataFrame
) -> None:
    with (
        patch("dq_sus.infer_schema.infer_schema.SINAN") as mock_sinan,
        patch("dq_sus.infer_schema.infer_schema.pd.read_parquet") as mock_read_parquet,
    ):
        mock_sinan_instance = MagicMock()
        mock_sinan.return_value = mock_sinan_instance
        mock_sinan_instance.load.return_value = mock_sinan_instance
        mock_sinan_instance.get_files.return_value = "mock_file"
        mock_read_parquet.return_value = mock_data

        data = extract_to_infer_schema("CHIK", 2023, mock_raw_data_path)
        mock_sinan_instance.download.assert_called_once_with(
            "mock_file", local_dir=str(mock_raw_data_path)
        )
        mock_read_parquet.assert_called_once()
        pd.testing.assert_frame_equal(data, mock_data)


def test_infer_and_save_schema(mock_schema_path: Path, mock_data: pd.DataFrame) -> None:
    schema_name = "test_schema"
    schema_file = mock_schema_path / f"{schema_name}.py"
    mock_schema_path.mkdir(parents=True, exist_ok=True)

    with patch("dq_sus.infer_schema.infer_schema.pa.infer_schema") as mock_infer_schema:
        mock_schema = MagicMock()
        mock_infer_schema.return_value = mock_schema
        mock_schema.to_script.return_value = "mock_schema_script"

        infer_and_save_schema(mock_data, schema_name, mock_schema_path)
        mock_infer_schema.assert_called_once_with(mock_data)
        with open(schema_file, "r", encoding="utf-8") as file:
            assert file.read() == "mock_schema_script"

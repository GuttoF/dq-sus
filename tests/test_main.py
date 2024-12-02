from unittest.mock import MagicMock, patch
import argparse

import pytest

from main import main, run_pipeline


@pytest.fixture
def mock_extractor() -> MagicMock: # type: ignore
    with patch("main.Extractor") as MockExtractor:
        mock_extractor = MockExtractor.return_value
        mock_extractor.extract_parquet.return_value = ["file1.parquet", "file2.parquet"]
        yield mock_extractor # type: ignore


@pytest.fixture
def mock_column_transformer() -> MagicMock: # type: ignore
    with patch("main.ColumnTransformer") as MockColumnTransformer:
        yield MockColumnTransformer.return_value # type: ignore


@pytest.fixture
def mock_db_transformer() -> MagicMock: # type: ignore
    with patch("main.DBTransformer") as MockDBTransformer:
        yield MockDBTransformer.return_value # type: ignore


@pytest.fixture
def mock_loader() -> MagicMock: # type: ignore
    with patch("main.Loader") as MockLoader:
        mock_loader = MockLoader.return_value
        mock_loader.load_data.return_value = MagicMock()
        yield mock_loader # type: ignore


def test_run_pipeline(
    mock_extractor: MagicMock,
    mock_column_transformer: MagicMock,
    mock_db_transformer: MagicMock,
    mock_loader: MagicMock
) -> None:
    run_pipeline(disease="CHIK", years=[2022, 2023], table_name="sinan", limit=10)

    mock_extractor.extract_parquet.assert_called_once_with("CHIK", [2022, 2023])
    mock_extractor.insert_parquet_to_duck.assert_called_once_with(
        ["file1.parquet", "file2.parquet"]
    )
    mock_column_transformer.rename_db_columns.assert_called_once()
    mock_db_transformer.transform_db.assert_called_once()
    mock_loader.load_data.assert_called_once_with(table_name="sinan", limit=10)


def test_main() -> None:
    with (
        patch("main.run_pipeline") as mock_run_pipeline,
        patch(
            "argparse.ArgumentParser.parse_args",
            return_value=argparse.Namespace(
                disease="CHIK", years=[2022, 2023], table_name="sinan", limit=10
            ),
        ),
    ):
        main()
        mock_run_pipeline.assert_called_once_with(
            disease="CHIK", years=[2022, 2023], table_name="sinan", limit=10
        )

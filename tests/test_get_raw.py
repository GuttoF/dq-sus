from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from dq_sus.extract.get_raw import Extractor


@pytest.fixture
def extractor() -> Extractor:
    return Extractor(
        db_path=Path("/tmp/test_db.duckdb"), parquet_path=Path("/tmp/parquet")
    )


def test_invalid_disease(extractor: Extractor) -> None:
    with pytest.raises(ValueError):
        extractor.extract_parquet("INVALID", 2022)


@patch("dq_sus.extract.get_raw.pd.read_parquet")
@patch("dq_sus.extract.get_raw.duckdb.connect")
def test_insert_parquet_to_duck(
    mock_connect: MagicMock, mock_read_parquet: MagicMock, extractor: Extractor
) -> None:
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    mock_read_parquet.return_value = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

    files = [Path("/tmp/parquet/CHIKBR22.parquet")]
    extractor.insert_parquet_to_duck(files)

    mock_connect.assert_called_once_with("/tmp/test_db.duckdb")
    mock_conn.register.assert_called_once_with(
        "temp_table", mock_read_parquet.return_value
    )
    mock_conn.execute.assert_any_call("CREATE TABLE sinan AS SELECT * FROM temp_table")
    mock_conn.unregister.assert_called_once_with("temp_table")
    mock_conn.close.assert_called_once()

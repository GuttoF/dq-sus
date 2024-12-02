import json
from pathlib import Path
from unittest.mock import patch

import duckdb
import pytest

from dq_sus.transform.transform_columns import ColumnTransformer


@pytest.fixture
def setup_db(tmp_path: Path) -> Path:  # type: ignore
    db_path = tmp_path / "test.db"
    conn = duckdb.connect(str(db_path))
    conn.execute("CREATE TABLE sinan (col1 VARCHAR, col2 VARCHAR)")
    conn.execute("INSERT INTO sinan VALUES ('áéíóú', 'çñ')")
    conn.close()
    return db_path


@pytest.fixture
def setup_json(tmp_path: Path) -> Path:
    json_path = tmp_path / "columns_translated_english.json"
    with open(json_path, "w") as f:
        json.dump({"col1": "vowels", "col2": "consonants"}, f)
    return json_path


def test_load_json_success(setup_json: Path) -> None:
    transformer = ColumnTransformer(json_path=setup_json.parent)
    result = transformer.load_json()
    assert result == {"col1": "vowels", "col2": "consonants"}


def test_load_json_file_not_found(tmp_path: Path) -> None:
    transformer = ColumnTransformer(json_path=tmp_path)
    with pytest.raises(FileNotFoundError):
        transformer.load_json()


def test_load_json_invalid_json(tmp_path: Path) -> None:
    json_path = tmp_path / "columns_translated_english.json"
    with open(json_path, "w") as f:
        f.write("invalid json")
    transformer = ColumnTransformer(json_path=tmp_path)
    with pytest.raises(json.JSONDecodeError):
        transformer.load_json()


def test_rename_db_columns(setup_db: Path, setup_json: Path) -> None:
    transformer = ColumnTransformer(db_path=setup_db, json_path=setup_json.parent)
    transformer.rename_db_columns()
    conn = duckdb.connect(str(setup_db))
    result = conn.execute("DESCRIBE sinan").fetchall()
    conn.close()
    result_column_names = [row[0] for row in result]
    expected_columns = ["vowels", "consonants"]
    assert result_column_names == expected_columns


def test_rename_db_columns_db_not_found(tmp_path: Path, setup_json: Path) -> None:
    transformer = ColumnTransformer(
        db_path=tmp_path / "non_existent.db", json_path=setup_json.parent
    )
    with pytest.raises(FileNotFoundError):
        transformer.rename_db_columns()


def test_rename_db_columns_unmapped_columns(setup_db: Path, tmp_path: Path) -> None:
    json_path = tmp_path / "columns_translated_english.json"
    with open(json_path, "w") as f:
        json.dump({"nonexistent": "newname"}, f)

    transformer = ColumnTransformer(db_path=setup_db, json_path=tmp_path)
    with patch("logging.warning") as mock_warning:
        transformer.rename_db_columns()
        mock_warning.assert_called_with(" - nonexistent")

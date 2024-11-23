import json
import logging
from pathlib import Path
from typing import Dict

import duckdb
import unidecode

from dq_sus.utils.config import DB_PATH, JSON_PATH

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_json(
    json_path: Path = JSON_PATH / "columns_translated_english.json",
) -> Dict[str, str]:
    """
    Load a JSON file containing column mappings.
    """
    if not json_path.exists():
        logging.error(f"JSON file not found at {json_path}")
        raise FileNotFoundError(f"JSON file not found at {json_path}")

    try:
        with open(json_path, "r") as file:
            columns_mapping = json.load(file)
        logging.info(f"Column mapping loaded successfully from {json_path}.")
        return dict(columns_mapping)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON file: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error while loading JSON: {e}")
        raise


def rename_db_columns(db_path: Path = DB_PATH, table_name: str = "sinan") -> None:
    """
    Renames columns in a DuckDB table based on a JSON mapping and removes
    accents from column names.

    Args:
        db_path (Path): The path to the DuckDB database file.
        table_name (str, optional): The name of the table to rename columns in.
                                    Defaults to "sinan".

    Raises:
        FileNotFoundError: If the database file does not exist at the specified path.
        Exception: If there is an error during the renaming process, the transaction
                    is rolled back and the error is raised.

    Notes:
        - The function first removes accents from existing column names.
        - Then, it renames columns based on the provided JSON mapping.
        - If any columns in the JSON mapping are not found in the database,
            a warning is logged.
    """
    if not db_path.exists():
        logging.error(f"Database not found at {db_path}")
        raise FileNotFoundError(f"Database not found at {db_path}")

    column_mapping = load_json()

    try:
        conn = duckdb.connect(str(db_path))

        conn.begin()

        # Get existing columns and normalize them
        existing_columns = {
            col[0]: unidecode.unidecode(col[0])
            for col in conn.execute(f"DESCRIBE {table_name}").fetchall()
        }

        unmapped_columns = []

        # Remove accents from existing column names
        for col, normalized_col in existing_columns.items():
            if col != normalized_col:
                conn.execute(
                    f'ALTER TABLE {table_name} RENAME COLUMN "{col}" '
                    f'TO "{normalized_col}"'
                )
                logging.info(
                    f"Removed accents from column '{col}' to '{normalized_col}'"
                )

        for old_name, new_name in column_mapping.items():
            normalized_old_name = unidecode.unidecode(old_name)
            if normalized_old_name in existing_columns.values():
                conn.execute(
                    f'ALTER TABLE {table_name} RENAME COLUMN "{normalized_old_name}" '
                    f'TO "{new_name}"'
                )
                logging.info(f"Renamed column '{normalized_old_name}' to '{new_name}'.")
            else:
                unmapped_columns.append(old_name)

        conn.commit()
        conn.close()

        if unmapped_columns:
            logging.warning(
                "The following columns were not found in the JSON mapping or database "
                "and were not renamed:"
            )
            for col in unmapped_columns:
                logging.warning(f" - {col}")
        else:
            logging.info("All columns renamed successfully.")

    except Exception as e:
        logging.error(f"Error renaming columns in DuckDB: {e}")
        if conn:
            conn.rollback()
        raise


if __name__ == "__main__":
    rename_db_columns()

import json
import logging
from pathlib import Path
from typing import Dict

import duckdb
import unidecode

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

db_path = Path(__file__).resolve().parents[1] / "data" / "db" / "db.db"
json_dir = Path(__file__).resolve().parents[1] / "json"
json_paths = {
    "english": json_dir / "columns_translated_english.json",
    "portuguese": json_dir / "columns_translated_portuguese.json",
}


def load_json(language: str = "english") -> Dict[str, str]:
    if language not in json_paths:
        raise ValueError(
            "Language not supported. Please choose 'english' or 'portuguese'."
        )

    json_path = json_paths[language]

    try:
        with open(json_path, "r") as file:
            columns_mapping = json.load(file)
        logging.info(f"Column mapping for '{language}' loaded successfully.")
        return dict(columns_mapping)
    except FileNotFoundError:
        logging.error(f"JSON file for '{language}' not found in {json_path}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON file: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise


def rename_db_columns(
    db_path: Path, table_name: str = "sinan", language: str = "english"
) -> None:
    if not db_path.exists():
        logging.error(f"Database not found at {db_path}")
        raise FileNotFoundError(f"Database not found at {db_path}")

    column_mapping = load_json(language)

    try:
        conn = duckdb.connect(str(db_path))

        existing_columns = [
            col[0] for col in conn.execute(f"DESCRIBE {table_name}").fetchall()
        ]

        unmapped_columns = []

        for col in existing_columns:
            normalized_col = unidecode.unidecode(col)
            if col != normalized_col:
                rename_query = f'RENAME COLUMN "{col}" TO "{normalized_col}"'
                logging.info(f"Executing: {rename_query}")
                conn.execute(rename_query)
                logging.info(
                    f"Removed accents from column '{col}' to '{normalized_col}'"
                )

        for normalized_old_name, new_name in column_mapping.items():
            if normalized_old_name in existing_columns:
                rename_query = f'RENAME COLUMN "{normalized_old_name}" TO "{new_name}"'
                logging.info(f"Executing: {rename_query}")
                conn.execute(rename_query)
            else:
                unmapped_columns.append(normalized_old_name)

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
        raise


if __name__ == "__main__":
    rename_db_columns(db_path, "sinan")
import logging
from pathlib import Path

import duckdb
import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

db_path = Path(__file__).resolve().parents[1] / "data" / "db" / "db.db"


def load_duckdb_data(table_name: str = "sinan") -> pd.DataFrame:
    if not db_path.exists():
        logging.error(f"Database not found at {db_path}")
        raise FileNotFoundError(f"Database not found at {db_path}")

    try:
        conn = duckdb.connect(str(db_path))
        query = f"SELECT * FROM {table_name}"
        logging.info(f"Loading data from table '{table_name}' in DuckDB database.")

        data = conn.execute(query).fetchdf()
        conn.close()

        logging.info("Data loaded successfully.")
        return data

    except Exception as e:
        logging.error(f"Error loading data from DuckDB: {e}")
        raise


if __name__ == "__main__":
    print(db_path)
    data = load_duckdb_data("sinan")
    print(data.head())

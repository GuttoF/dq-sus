import logging
from pathlib import Path
from typing import Optional

import duckdb
import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

db_path = Path(__file__).resolve().parents[1] / "data" / "db" / "db.db"


def load_duckdb_data(
    table_name: str = "sinan", limit: Optional[int] = None
) -> pd.DataFrame:
    """
    Load data from a DuckDB database table into a pandas DataFrame.
    Parameters:
    table_name (str): The name of the table to load data from. Defaults to "sinan".
    limit (Optional[int]): The maximum number of rows to load.
        If None, all rows are loaded. Defaults to None.
    Returns:
    pd.DataFrame: A DataFrame containing the data loaded from the specified
    DuckDB table.
    Raises:
    FileNotFoundError: If the DuckDB database file does not exist.
    Exception: If there is an error loading data from the DuckDB database.
    """

    if not db_path.exists():
        logging.error(f"Database not found at {db_path}")
        raise FileNotFoundError(f"Database not found at {db_path}")

    try:
        with duckdb.connect(str(db_path)) as conn:
            query = f"SELECT * FROM {table_name}"
            if limit:
                query += f" LIMIT {limit}"
            logging.info(f"Loading data from table '{table_name}' in DuckDB database.")

            data_arrow = conn.execute(query).fetch_arrow_table()
            data: pd.DataFrame = data_arrow.to_pandas()

            logging.info("Data loaded successfully.")
            return data

    except Exception as e:
        logging.error(f"Error loading data from DuckDB: {e}")
        raise


if __name__ == "__main__":
    data = load_duckdb_data("sinan", limit=100)
    print(data.head())

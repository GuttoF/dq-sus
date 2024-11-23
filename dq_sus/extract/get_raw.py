import logging
import os
from pathlib import Path
from typing import Union

import duckdb
import pandas as pd
from pysus.ftp.databases.sinan import SINAN

from dq_sus.utils.config import DB_PATH, PARQUET_PATH

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def extract_parquet(
    disease: str, years: Union[int, list[int]], file_path: Path = PARQUET_PATH
) -> list[Path]:
    """
    Extracts parquet files for a given disease and years.

    Parameters:
    disease (str): The disease to extract data for. Must be one of
        ["ZIKA", "CHIK", "DENG"].
    years (Union[int, list[int]]): The year or list of years to extract data for.
    file_path (Path, optional): The directory path where parquet files are stored.
        Defaults to PARQUET_PATH.

    Returns:
    list[Path]: A list of Paths to the extracted parquet files.

    Raises:
    ValueError: If an invalid disease is provided.
    """
    valid_diseases = ["ZIKA", "CHIK", "DENG"]
    if disease not in valid_diseases:
        logging.error(
            f"Invalid disease '{disease}' provided. Only {valid_diseases} "
            "are supported."
        )
        raise ValueError(
            f"Invalid disease '{disease}'. Please use one of the following: "
            f"{valid_diseases}"
        )

    if isinstance(years, int):
        years = [years]

    file_paths = []
    for year in years:
        year_suffix = str(year)[2:]
        file_name = file_path / f"{disease}BR{year_suffix}.parquet"

        if not file_name.exists():
            sinan = SINAN().load()
            file = sinan.get_files(disease, year)
            sinan.download(file, local_dir=str(file_path))
            logging.info(f"File saved in {file_name}")

        file_paths.append(file_name)

    return file_paths


def insert_parquet_to_duck(files: list[Path], file_path: Path = DB_PATH) -> None:
    """
    Inserts data from a list of Parquet files into a DuckDB database.

    This function creates a new DuckDB database at the specified file path,
    overwriting any existing database file. It then reads each Parquet file
    in the provided list, and inserts the data into a table named 'sinan'
    within the database. If the table already exists, the data is appended
    to the table.

    Args:
        files (list[Path]): A list of Path objects pointing to the Parquet files
            to be inserted.
        file_path (Path, optional): The directory path where the DuckDB
            database file will be created. Defaults to DB_PATH.

    Returns:
        None

    Raises:
        Exception: If an error occurs during the database operations,
        it logs the error and closes the connection.
    """
    duck_path = file_path
    if not duck_path.parent.exists():
        logging.info(f"Directory {duck_path.parent} does not exist. Creating it.")
        duck_path.parent.mkdir(parents=True, exist_ok=True)

    if duck_path.exists():
        logging.info(f"Database already exists at {duck_path}, it will be overwritten.")
        os.remove(duck_path)

    conn = None

    try:
        conn = duckdb.connect(str(duck_path))

        for i, file in enumerate(files):
            logging.info(f"Inserting data from {file} into the database.")
            data = pd.read_parquet(file)

            conn.register("temp_table", data)

            if i == 0:
                conn.execute("CREATE TABLE sinan AS SELECT * FROM temp_table")
            else:
                conn.execute("INSERT INTO sinan SELECT * FROM temp_table")

            conn.unregister("temp_table")
            del data

        conn.close()
        logging.info("All data inserted into the database successfully.")
    except Exception as e:
        logging.error(f"Error: {e}")
        if conn:
            conn.close()


if __name__ == "__main__":
    years = [2022, 2023]
    files = extract_parquet("CHIK", years)
    insert_parquet_to_duck(files)

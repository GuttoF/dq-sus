import logging
import warnings
from pathlib import Path
from typing import Union
import os
import duckdb
import pandas as pd
from pysus.ftp.databases.sinan import SINAN

warnings.filterwarnings("ignore", category=SyntaxWarning, module="stringcase")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

parquet_path = Path(__file__).resolve().parents[1] / "data" / "parquet"
parquet_path.mkdir(parents=True, exist_ok=True)

db_path = Path(__file__).resolve().parents[1] / "data" / "db"
db_path.mkdir(parents=True, exist_ok=True)


def extract_parquet(
    disease: str, years: Union[int, list[int]], file_path: Path = parquet_path
) -> list[Path]:
    valid = ["ZIKA", "CHIK", "DENG"]
    if disease not in valid:
        logging.error(
            f"Invalid disease '{disease}' provided. Only {valid} are supported."
        )
        raise ValueError(
            f"Invalid disease '{disease}'. Please use one of the following: {valid}"
        )

    if isinstance(years, int):
        years = [years]

    file_paths = []
    for year in years:
        year_str = str(year)[2:]
        file_name = file_path / f"{disease}BR{year_str}.parquet"

        if not file_name.exists():
            sinan = SINAN().load()
            file = sinan.get_files(disease, year)
            sinan.download(file, local_dir=str(file_path))
            logging.info(f"File saved in {file_path}")

        file_paths.append(file_name)

    return file_paths


def insert_parquet_to_duck(files: list[Path], file_path: Path = db_path) -> None:
    duck_path = file_path / "db.db"
    if duck_path.exists():
        logging.info("Database already exists, it will be overwritten.")
        os.remove(duck_path)

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

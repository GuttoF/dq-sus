import logging
import warnings
from pathlib import Path
from typing import Union

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
) -> pd.DataFrame:
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

    data_frames = []
    for year in years:
        year_str = str(year)[2:]
        file_name = file_path / f"{disease}BR{year_str}.parquet"

        if file_name.exists():
            logging.info(f"File located in {file_name} already exists, loading data.")
            data = pd.read_parquet(file_name)
        else:
            sinan = SINAN().load()
            file = sinan.get_files(disease, year)
            sinan.download(file, local_dir=str(file_path))
            logging.info(f"File saved in {file_path}")
            data = pd.read_parquet(file_name)

        data_frames.append(data)

    return pd.concat(data_frames, ignore_index=True)


def extract_to_duck(data: pd.DataFrame, file_path: Path = db_path) -> None:
    try:
        duck_path = file_path / "db.db"
        if duck_path.exists():
            logging.info("Database already exists, it will be overwritten.")

        conn = duckdb.connect(str(duck_path))
        conn.execute("CREATE TABLE IF NOT EXISTS sinan AS SELECT * FROM data")
        conn.close()
        logging.info("Database created")
    except Exception as e:
        logging.error(f"Error: {e}")


if __name__ == "__main__":
    years = [2022, 2023]
    data = extract_parquet("CHIK", years)
    extract_to_duck(data)

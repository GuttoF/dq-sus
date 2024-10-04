import logging
import warnings
from pathlib import Path

import pandas as pd
import pandera as pa
from pysus.ftp.databases.sinan import SINAN

warnings.filterwarnings("ignore", category=SyntaxWarning, module="stringcase")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

path = Path(__file__).resolve().parents[2] / "data" / "raw"
path.mkdir(parents=True, exist_ok=True)

schema_path = Path(__file__).resolve().parents[1] / "schemas"
schema_path.mkdir(parents=True, exist_ok=True)


def extract_to_infer_schema(
    disease: str, year: int, file_path: Path = path
) -> pd.DataFrame:
    year_str = str(year)[2:]
    file_name = path / f"{disease}BR{year_str}.parquet"

    if file_name.exists():
        logging.info(f"File located in {file_name} already exists, stopping execution.")
        data = pd.read_parquet(file_name)
        return data

    sinan = SINAN().load()
    file = sinan.get_files(disease, year)
    sinan.download(file, local_dir=str(file_path))
    logging.info(f"Arquivo salvo em {file_path}")
    data = pd.read_parquet(file_name)
    return data


if __name__ == "__main__":
    data = extract_to_infer_schema("CHIK", 2023)
    schema = pa.infer_schema(data)

    schema_file = schema_path / "model_schema.py"
    with open(schema_file, "w", encoding="utf-8") as file:
        file.write(schema.to_script()) # type: ignore

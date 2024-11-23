from dq_sus.extract import extract_parquet, insert_parquet_to_duck
from dq_sus.transform import rename_db_columns, transform_db
from dq_sus.load import load_duckdb_data


def main() -> None:
    years = [2022, 2023]
    files = extract_parquet("CHIK", years)
    insert_parquet_to_duck(files)
    rename_db_columns()
    transform_db()
    data = load_duckdb_data(table_name="alarms_severities", limit=100)
    print(data.head())



if __name__ == "__main__":
    main()

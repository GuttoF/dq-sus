from dq_sus.extract import Extractor
from dq_sus.transform import ColumnTransformer, DBTransformer
from dq_sus.load import Loader


def main() -> None:
    extractor = Extractor()
    column_transformer = ColumnTransformer()
    db_transformer = DBTransformer()
    db_loader = Loader()

    years = [2022, 2023]
    files = extractor.extract_parquet("CHIK", years)
    extractor.insert_parquet_to_duck(files)
    column_transformer.rename_db_columns()
    db_transformer.transform_db()
    data = db_loader.load_data(table_name="alarms_severities", limit=100)

    print(data.head())


if __name__ == "__main__":
    main()

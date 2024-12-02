import argparse
from dq_sus.extract import Extractor
from dq_sus.transform import ColumnTransformer, DBTransformer
from dq_sus.load import Loader


def run_pipeline(disease: str, years: list[int], table_name: str, limit: int) -> None:
    """
    Run the complete ETL pipeline.

    Args:
        disease (str): Disease to process (e.g., "CHIK").
        years (list[int]): List of years to process (e.g., [2022, 2023]).
        table_name (str): Name of the table to load from the database.
        limit (int): Number of rows to load from the table.
    """
    extractor = Extractor()
    column_transformer = ColumnTransformer()
    db_transformer = DBTransformer()
    db_loader = Loader()

    print("Starting pipeline...")
    files = extractor.extract_parquet(disease, years)
    extractor.insert_parquet_to_duck(files)
    column_transformer.rename_db_columns()
    db_transformer.transform_db()
    data = db_loader.load_data(table_name=table_name, limit=limit)

    print("Pipeline completed. Sample data:")
    print(data.head())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the ETL pipeline for SINAN data."
    )

    # CLI arguments
    parser.add_argument(
        "--disease",
        type=str,
        required=True,
        help="Disease to process (e.g., 'CHIK', 'ZIKA', 'DENG').",
    )
    parser.add_argument(
        "--years",
        type=int,
        nargs="+",
        required=True,
        help="List of years to process (e.g., 2022 2023).",
    )
    parser.add_argument(
        "--table_name",
        type=str,
        default="alarms_severities",
        help=(
            "Name of the table to load from the database "
            "(default: 'alarms_severities')."
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Number of rows to load from the table (default: 100).",
    )

    args = parser.parse_args()

    # Run the pipeline
    run_pipeline(
        disease=args.disease,
        years=args.years,
        table_name=args.table_name,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()

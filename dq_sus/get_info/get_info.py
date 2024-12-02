import logging

import pandas as pd

from dq_sus.extract import Extractor
from dq_sus.load import Loader
from dq_sus.transform import ColumnTransformer, DBTransformer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_data_from_table(
    table_name: str,
    years: list[int] = [2022, 2023],
    disease: str = "CHIK",
    limit: int | None = None,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Extracts data from a specified table, processes it, and returns it as a pandas
    DataFrame.

    Parameters:
    table_name (str): The name of the table to load data from.
    years (list[int], optional): List of years to filter the data. Defaults to [2022,
    2023].
    disease (str, optional): Disease code to filter the data. Defaults to "CHIK".
    limit (int | None, optional): Maximum number of rows to load. If None, loads all
    rows. Defaults to None.
    verbose (bool, optional): If True, enables verbose logging. Defaults to False.

    Returns:
    pd.DataFrame: The processed data as a pandas DataFrame. Returns an empty DataFrame
    if no data is available.
    """
    if not verbose:
        logging.disable(logging.CRITICAL)

    try:
        extractor = Extractor()
        column_transformer = ColumnTransformer()
        db_transformer = DBTransformer()
        db_loader = Loader()

        files = extractor.extract_parquet(disease, years)
        extractor.insert_parquet_to_duck(files)
        column_transformer.rename_db_columns()
        db_transformer.transform_db()
        data = db_loader.load_data(table_name=table_name, limit=limit)

        data = data.dropna(axis=1, how="all")

        if data.empty or data.shape[1] == 0:
            logging.warning("No data available: All columns are empty or null.")
            return pd.DataFrame()

        data = data.dropna()

        if data.empty:
            logging.warning(
                "No data available: All rows are empty or null after filtering."
            )
            return pd.DataFrame()
    finally:
        if not verbose:
            logging.disable(logging.NOTSET)

    return data


def get_notifications(
    years: list[int] = [2022, 2023], disease: str = "CHIK", limit: int | None = None
) -> pd.DataFrame:
    """
    Retrieve notification data for a specified disease and years.

    Args:
        years (list[int], optional): List of years to retrieve data for. Defaults to
        [2022, 2023].
        disease (str, optional): Disease code to filter notifications.
        Defaults to "CHIK".
        limit (int | None, optional): Maximum number of records to retrieve. Defaults
        to None.

    Returns:
        pd.DataFrame: DataFrame containing the notification data.
    """
    return get_data_from_table("notifications_info", years, disease, limit)


def get_personal_data(
    years: list[int] = [2022, 2023], disease: str = "CHIK", limit: int | None = None
) -> pd.DataFrame:
    """
    Retrieve patients personal data for a specified disease and years.

    Args:
        years (list[int], optional): List of years to retrieve data for. Defaults to
        [2022, 2023].
        disease (str, optional): Disease code to filter notifications.
        Defaults to "CHIK".
        limit (int | None, optional): Maximum number of records to retrieve.
        Defaults to None.

    Returns:
        pd.DataFrame: DataFrame containing the notification data.
    """
    return get_data_from_table("personal_data", years, disease, limit)


def get_clinical_signs(
    years: list[int] = [2022, 2023], disease: str = "CHIK", limit: int | None = None
) -> pd.DataFrame:
    """
    Retrieve clinical signs data data for a specified disease and years.

    Args:
        years (list[int], optional): List of years to retrieve data for.
        Defaults to [2022, 2023].
        disease (str, optional): Disease code to filter notifications.
        Defaults to "CHIK".
        limit (int | None, optional): Maximum number of records to retrieve.
        Defaults to None.

    Returns:
        pd.DataFrame: DataFrame containing the notification data.
    """
    return get_data_from_table("clinical_signs", years, disease, limit)


def get_patient_diseases(
    years: list[int] = [2022, 2023], disease: str = "CHIK", limit: int | None = None
) -> pd.DataFrame:
    """
    Retrieve patient diseases for a specified disease and years.

    Args:
        years (list[int], optional): List of years to retrieve data for. Defaults to
        [2022, 2023].
        disease (str, optional): Disease code to filter notifications.
        Defaults to "CHIK".
        limit (int | None, optional): Maximum number of records to retrieve.
        Defaults to None.

    Returns:
        pd.DataFrame: DataFrame containing the notification data.
    """
    return get_data_from_table("patient_diseases", years, disease, limit)


def get_exams(
    years: list[int] = [2022, 2023], disease: str = "CHIK", limit: int | None = None
) -> pd.DataFrame:
    """
    Retrieve exams info for a specified disease and years.

    Args:
        years (list[int], optional): List of years to retrieve data for.
        Defaults to [2022, 2023].
        disease (str, optional): Disease code to filter notifications.
        Defaults to "CHIK".
        limit (int | None, optional): Maximum number of records to retrieve.
        Defaults to None.

    Returns:
        pd.DataFrame: DataFrame containing the notification data.
    """
    return get_data_from_table("exams", years, disease, limit)


def get_hospital_info(
    years: list[int] = [2022, 2023], disease: str = "CHIK", limit: int | None = None
) -> pd.DataFrame:
    """
    Retrieve hospital info for a specified disease and years.

    Args:
        years (list[int], optional): List of years to retrieve data for.
        Defaults to [2022, 2023].
        disease (str, optional): Disease code to filter notifications.
        Defaults to "CHIK".
        limit (int | None, optional): Maximum number of records to retrieve.
        Defaults to None.

    Returns:
        pd.DataFrame: DataFrame containing the notification data.
    """
    return get_data_from_table("hospital_info", years, disease, limit)


def get_alarm_severities(
    years: list[int] = [2022, 2023], disease: str = "CHIK", limit: int | None = None
) -> pd.DataFrame:
    """
    Retrieve alarm severities in treatment for a specified disease and years.

    Args:
        years (list[int], optional): List of years to retrieve data for.
        Defaults to [2022, 2023].
        disease (str, optional): Disease code to filter notifications.
        Defaults to "CHIK".
        limit (int | None, optional): Maximum number of records to retrieve.
        Defaults to None.

    Returns:
        pd.DataFrame: DataFrame containing the notification data.
    """
    return get_data_from_table("alarms_severities", years, disease, limit)


def get_sinan_info(
    years: list[int] = [2022, 2023], disease: str = "CHIK", limit: int | None = None
) -> pd.DataFrame:
    """
    Retrieve sinal internal info for a specified disease and years.

    Args:
        years (list[int], optional): List of years to retrieve data for.
        Defaults to [2022, 2023].
        disease (str, optional): Disease code to filter notifications.
        Defaults to "CHIK".
        limit (int | None, optional): Maximum number of records to retrieve.
        Defaults to None.

    Returns:
        pd.DataFrame: DataFrame containing the notification data.
    """
    return get_data_from_table("sinan_internal_info", years, disease, limit)

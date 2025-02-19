import pandas as pd

from src.utils.csv_parser import CSVParser

parser = CSVParser()


def _validate(data: pd.DataFrame) -> pd.DataFrame:
    data["is_good"] = 1
    return data


def validate_data(file_path: str) -> pd.DataFrame:
    df = parser.read_csv_from_file_path(file_path)
    return _validate(df)

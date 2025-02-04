import pandas as pd
from typing import List
import great_expectations as gx


class ValidationManager:
    def __init__(self):
        self.df = None
        self.expectations = []
        context = gx.get_context()

    @staticmethod
    def check_col_names(df: pd.DataFrame, col_names: List) -> bool:
        return all(col in df.columns for col in col_names)

    @staticmethod
    def check_data_types(df: pd.DataFrame, col_types: dict) -> bool:
        return df.dtypes.to_dict() == col_types

    @staticmethod
    def _find_null_rows(df: pd.DataFrame) -> List:
        null_rows = df[df.isnull().any(axis=1)].index.tolist()
        return null_rows

    def find_invalid_rows(self, df: pd.DataFrame) -> List:
        invalid_indices = []
        invalid_indices.extend(self._find_null_rows(df))
        return invalid_indices

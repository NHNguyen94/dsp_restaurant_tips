from typing import List

import pandas as pd

from src.api.v1.models.prediction_request import PredictionRequest


class ValidationManager:
    @staticmethod
    def validate_none_json_request(request: PredictionRequest) -> bool:
        return all(value is None for value in request.dict().values())

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

    @staticmethod
    def find_invalid_rows(df: pd.DataFrame) -> List:
        invalid_indices = []
        invalid_indices.extend(ValidationManager._find_null_rows(df))
        return invalid_indices

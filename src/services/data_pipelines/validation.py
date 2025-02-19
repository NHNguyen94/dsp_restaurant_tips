from typing import Dict

import great_expectations as gx
import pandas as pd
from great_expectations.datasource.fluent.interfaces import Batch

from src.utils.configs_manager import DataConfigs
from src.utils.csv_parser import CSVParser


class ValidationService:
    def __init__(self, file_path: str):
        self.parser = CSVParser()
        self.df = self.parser.read_csv_from_file_path(file_path)
        self.expected_data = DataConfigs.EXPECTED_RESULTS_FOR_VALIDATION

    def _get_gx_batch(self) -> Batch:
        context = gx.get_context()
        data_source = context.data_sources.add_pandas(name="data")
        data_asset = data_source.add_dataframe_asset(name="pd DF asset")
        batch_def = data_asset.add_batch_definition_whole_dataframe("batch_definition")
        batch = batch_def.get_batch(batch_parameters={"dataframe": self.df})
        return batch

    def validate_columns(self) -> Dict:
        cols_results = {}
        for k, v in self.expected_data.items():
            if "min" in v and "max" in v:
                expectation = gx.expectations.ExpectColumnValuesToBeBetween(
                    column=k,
                    min_value=v["min"],
                    max_value=v["max"]
                )
                result = self._get_gx_batch().validate(expectation)
                cols_results[k] = result
            if "accept" in v:
                expectation = gx.expectations.ExpectColumnDistinctValuesToBeInSet(
                    column=k,
                    value_set=v["accept"]
                )
                result = self._get_gx_batch().validate(expectation)
                cols_results[k] = result
        return cols_results

    # def _validate(data: pd.DataFrame) -> pd.DataFrame:
    #     data["is_good"] = 1
    #     return data

    def run_validate_data(self, file_path: str) -> pd.DataFrame:
        df = self.parser.read_csv_from_file_path(file_path)
        return df
        # return _validate(df)

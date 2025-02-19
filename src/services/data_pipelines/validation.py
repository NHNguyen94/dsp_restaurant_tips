from typing import Dict, List

import great_expectations as gx
import pandas as pd
from great_expectations.core import ExpectationSuite
from great_expectations.datasource.fluent.interfaces import Batch
from great_expectations.execution_engine import PandasExecutionEngine
from great_expectations.validator.validator import Validator
from great_expectations.datasource.fluent.pandas_datasource import PandasDatasource

from src.utils.configs_manager import DataConfigs
from src.utils.csv_parser import CSVParser


class ValidationService:
    def __init__(self, file_path: str, batch_definition: str):
        self.batch_definition = batch_definition
        self.parser = CSVParser()
        self.df = self.parser.read_csv_from_file_path(file_path)
        self.expected_data = DataConfigs.EXPECTED_RESULTS_FOR_VALIDATION
        self.context = gx.get_context()

    def _get_gx_batch(self) -> Batch:
        data_source = self.context.data_sources.add_pandas(name="data")
        data_asset = data_source.add_dataframe_asset(name="pd DF asset")
        batch_def = data_asset.add_batch_definition_whole_dataframe(
            self.batch_definition
        )
        return batch_def.get_batch(batch_parameters={"dataframe": self.df})

    # https://github.com/great-expectations/great_expectations/blob/develop/tests/validator/test_validator.py
    def _get_gx_validator(self) -> Validator:
        batch = self._get_gx_batch()
        return Validator(execution_engine=PandasExecutionEngine(), batches=[batch])

    def validate_columns_with_validator(self):
        validator = self._get_gx_validator()
        suite_name = "validation_suite"
        validator.expectation_suite_name = suite_name
        suite = self.context.suites.add(ExpectationSuite(suite_name))
        cols_results = {}
        for k, v in self.expected_data.items():
            if "min" in v and "max" in v:
                expectation = gx.expectations.ExpectColumnValuesToBeBetween(
                    column=k, min_value=v["min"], max_value=v["max"]
                )
                suite.add_expectation(expectation)
            if "accept" in v:
                expectation = gx.expectations.ExpectColumnValuesToBeInSet(
                    column=k, value_set=v["accept"]
                )
                suite.add_expectation(expectation)

        # Save and build Datadocs
        # validator.save_expectation_suite(discard_failed_expectations=False)
        self.context.build_data_docs()
        self.context.open_data_docs()

        results = validator.validate(suite)
        return results

    def validate_columns(self) -> Dict:
        batch = self._get_gx_batch()
        cols_results = {}
        for k, v in self.expected_data.items():
            if "min" in v and "max" in v:
                expectation = gx.expectations.ExpectColumnValuesToBeBetween(
                    column=k, min_value=v["min"], max_value=v["max"]
                )
                result = batch.validate(expectation)
                cols_results[k] = result
            if "accept" in v:
                expectation = gx.expectations.ExpectColumnValuesToBeInSet(
                    column=k, value_set=v["accept"]
                )
                result = batch.validate(expectation)
                cols_results[k] = result

        # Build datadocs
        # print("Checking if the site names are available")
        # print(self.context.get_site_names())
        # print(self.context.get_docs_sites_urls())
        #
        # self.context.build_data_docs()
        # self.context.open_data_docs()


        return cols_results

    def get_failed_indices(self, cols_results: Dict) -> List[int]:
        unique_failed_indicies = []
        cols = self.expected_data.keys()
        for col in cols:
            if cols_results[col]["success"] == False:
                failed_indices = cols_results[col]["result"][
                    "partial_unexpected_index_list"
                ]
                unique_failed_indicies.extend(failed_indices)
        unique_failed_indicies = set(unique_failed_indicies)
        return list(unique_failed_indicies)

    def add_is_good_column(self) -> pd.DataFrame:
        failed_indices = self.get_failed_indices(self.validate_columns())
        new_df = self.df.copy()
        if len(failed_indices) > 0:
            new_df["is_good"] = 1
            new_df.loc[failed_indices, "is_good"] = 0
        else:
            new_df["is_good"] = 1

        return new_df

    def validate_data(self) -> pd.DataFrame:
        new_df = self.add_is_good_column()
        return new_df


def run_validate_data(file_path: str, batch_definition: str) -> pd.DataFrame:
    validation_service = ValidationService(file_path, batch_definition)
    return validation_service.validate_data()

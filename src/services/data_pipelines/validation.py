from typing import Dict, List

import great_expectations as gx
import pandas as pd
from great_expectations import RunIdentifier
from great_expectations.core import (
    ExpectationSuite,
    ExpectationValidationResult,
    ExpectationSuiteValidationResult,
)
from great_expectations.data_context.types.resource_identifiers import (
    ValidationResultIdentifier,
    ExpectationSuiteIdentifier,
)
from great_expectations.datasource.fluent.interfaces import Batch
from great_expectations.execution_engine import PandasExecutionEngine
from great_expectations.validator.validator import Validator

from services.data_pipelines.models.validated_result import ValidatedResult
from src.utils.configs_manager import DataConfigs
from src.utils.csv_parser import CSVParser
from src.utils.date_time_manager import DateTimeManager


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

    def _build_datadocs_urls(
        self, results: ExpectationValidationResult | ExpectationSuiteValidationResult
    ) -> List:
        suite_identifier = ExpectationSuiteIdentifier(
            name=results.meta["expectation_suite_name"]
        )
        validation_result_identifier = ValidationResultIdentifier(
            expectation_suite_identifier=suite_identifier,
            run_id=RunIdentifier(),
            batch_identifier=str(DateTimeManager.get_current_local_time()),
        )
        self.context.validation_results_store.set(validation_result_identifier, results)
        self.context.build_data_docs()
        docs_urls = self.context.get_docs_sites_urls()
        docs_urls = [url["site_url"] for url in docs_urls]
        return docs_urls

    def _parse_results_from_validator(
        self, results: ExpectationValidationResult | ExpectationSuiteValidationResult
    ) -> (List, bool):
        parsed_results = []
        overall_result = results["success"]
        results = results["results"]
        for result in results:
            details = {
                "success": result["success"],
                "column": result["expectation_config"]["kwargs"]["column"],
                "result": result["result"],
            }
            parsed_results.append(details)
        return (parsed_results, overall_result)

    def validate_columns_with_validator(
        self,
    ) -> ExpectationValidationResult | ExpectationSuiteValidationResult:
        validator = self._get_gx_validator()
        suite_name = "validation_suite"
        validator.expectation_suite_name = suite_name
        suite = self.context.suites.add(ExpectationSuite(suite_name))
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

        return validator.validate(suite)

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

    # def add_is_good_column(self) -> pd.DataFrame:
    #     failed_indices = self.get_failed_indices(self.validate_columns())
    #     new_df = self.df.copy()
    #     if len(failed_indices) > 0:
    #         new_df["is_good"] = 1
    #         new_df.loc[failed_indices, "is_good"] = 0
    #     else:
    #         new_df["is_good"] = 1
    #
    #     return new_df

    def _create_filter_conditions(self, parsed_results: List) -> List:
        filter_conditions = []
        for res in parsed_results:
            if res["success"] == False:
                filter = {
                    "column": res["column"],
                    "values_to_remove": res["result"]["partial_unexpected_list"],
                }
                filter_conditions.append(filter)

        return filter_conditions

    def _make_df_with_is_good_col(self, parsed_results: List) -> pd.DataFrame:
        new_df = self.df.copy()
        filter_conditions = self._create_filter_conditions(parsed_results)
        if len(filter_conditions) > 0:
            new_df["is_good"] = 1
            for filter in filter_conditions:
                new_df.loc[
                    new_df[filter["column"]].isin(filter["values_to_remove"]), "is_good"
                ] = 0
        else:
            new_df["is_good"] = 1

        return new_df

    def validate_data(self) -> ValidatedResult:
        validated_result = self.validate_columns_with_validator()
        docs_urls = self._build_datadocs_urls(validated_result)
        (parsed_results, overall_result) = self._parse_results_from_validator(
            validated_result
        )
        final_df = self._make_df_with_is_good_col(parsed_results)
        return ValidatedResult(parsed_results, overall_result, docs_urls, final_df)


def run_validate_data(file_path: str, batch_definition: str) -> ValidatedResult:
    validation_service = ValidationService(file_path, batch_definition)
    return validation_service.validate_data()

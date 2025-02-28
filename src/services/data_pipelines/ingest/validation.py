from typing import List, Union

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

from src.services.data_pipelines.models import (
    ValidatedResult,
    GXResultPerColumn,
    GXResultNotNullDetails,
    GXResultBetweenOrInSetDetails,
    OverallStatistics,
    AllResults,
)
from src.utils.configs_manager import DataConfigs
from src.utils.csv_parser import CSVParser
from src.utils.date_time_manager import DateTimeManager


class ValidationService:
    def __init__(self, file_path: str, batch_definition: str):
        self.file_path = file_path
        self.batch_definition = batch_definition
        self.parser = CSVParser()
        self.df = self.parser.read_csv_from_file_path(self.file_path)
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
        self,
        results: Union[ExpectationValidationResult, ExpectationSuiteValidationResult],
    ) -> List:
        suite_identifier = ExpectationSuiteIdentifier(
            name=results.meta["expectation_suite_name"]
        )
        validation_result_identifier = ValidationResultIdentifier(
            expectation_suite_identifier=suite_identifier,
            run_id=RunIdentifier(),
            batch_identifier=str(DateTimeManager.get_current_local_time_str()),
        )
        self.context.validation_results_store.set(validation_result_identifier, results)
        self.context.build_data_docs()
        docs_urls = self.context.get_docs_sites_urls()
        docs_urls = [url["site_url"] for url in docs_urls]
        return docs_urls

    def _parse_results_from_validator(
        self,
        input_results: Union[
            ExpectationValidationResult, ExpectationSuiteValidationResult
        ],
    ) -> (List[GXResultPerColumn], bool, OverallStatistics):
        parsed_results = []
        overall_result = input_results["success"]
        stats = OverallStatistics(**input_results["statistics"])

        results = input_results["results"]
        for res in results:
            expectation_config = res["expectation_config"]
            data_per_col = GXResultPerColumn(
                success=res["success"],
                column=expectation_config["kwargs"]["column"],
                all_results=AllResults(),
            )

            if expectation_config["type"] == "expect_column_to_exist":
                data_per_col.all_results.result_column_exist = res["success"]
            if expectation_config["type"] == "expect_column_values_to_not_be_null":
                data_per_col.all_results.result_not_null = GXResultNotNullDetails(
                    **res["result"]
                )
            if expectation_config["type"] in [
                "expect_column_values_to_be_in_set",
                "expect_column_values_to_be_between",
            ]:
                data_per_col.all_results.result_between_or_in_set = (
                    GXResultBetweenOrInSetDetails(**res["result"])
                )

            parsed_results.append(data_per_col)

        return (parsed_results, overall_result, stats)

    def group_by_parsed_results_by_column(
        self, parsed_results: List[GXResultPerColumn]
    ) -> List[GXResultPerColumn]:
        grouped_results = []
        for col in self.expected_data.keys():
            final_success_for_column = True
            new_all_res = AllResults()
            for res in parsed_results:
                if res.column == col:
                    if res.all_results.result_column_exist:
                        new_all_res.result_column_exist = (
                            res.all_results.result_column_exist
                        )
                        final_success_for_column = (
                            final_success_for_column and res.success
                        )
                    if res.all_results.result_not_null:
                        new_all_res.result_not_null = res.all_results.result_not_null
                        final_success_for_column = (
                            final_success_for_column and res.success
                        )
                    if res.all_results.result_between_or_in_set:
                        new_all_res.result_between_or_in_set = (
                            res.all_results.result_between_or_in_set
                        )
                        final_success_for_column = (
                            final_success_for_column and res.success
                        )
            new_parsed_res = GXResultPerColumn(
                success=final_success_for_column, column=col, all_results=new_all_res
            )
            grouped_results.append(new_parsed_res)

        for data in grouped_results:
            if (
                data.all_results.result_column_exist is None
                or data.all_results.result_not_null is None
                or data.all_results.result_between_or_in_set is None
            ):
                raise ValueError("Missing validation category")

        return grouped_results

    def validate_columns_with_validator(
        self,
    ) -> Union[ExpectationValidationResult, ExpectationSuiteValidationResult]:
        validator = self._get_gx_validator()
        suite_name = "validation_suite"
        validator.expectation_suite_name = suite_name
        suite = self.context.suites.add(ExpectationSuite(suite_name))
        # print(f"\n\n\nself.expected_data: {self.expected_data}\n\n\n")
        for k, v in self.expected_data.items():
            expectation_col = gx.expectations.ExpectColumnToExist(column=k)
            suite.add_expectation(expectation_col)
            expectation_value = gx.expectations.ExpectColumnValuesToNotBeNull(column=k)
            suite.add_expectation(expectation_value)
            if "min" in v and "max" in v:
                expectation = gx.expectations.ExpectColumnValuesToBeBetween(
                    column=k, min_value=v["min"], max_value=v["max"]
                )
                suite.add_expectation(expectation)
            if "accept" in v:
                # print(f'v_accept: {v["accept"]}, with type: {type(v["accept"])}')
                expectation = gx.expectations.ExpectColumnValuesToBeInSet(
                    column=k,
                    value_set=list(
                        v["accept"]
                    ),  # For old version, tuple is not accepted, has to be set/list
                )
                suite.add_expectation(expectation)

        return validator.validate(suite)

    def _create_filter_conditions(
        self, parsed_results: List[GXResultPerColumn]
    ) -> List:
        filter_conditions = []
        for res in parsed_results:
            if res.success == False:
                filter = {
                    "column": res.column,
                    "values_to_remove": res.all_results.result_between_or_in_set.partial_unexpected_list,
                }
                filter_conditions.append(filter)

        return filter_conditions

    def _make_df_with_is_good_col(
        self, parsed_results: List[GXResultPerColumn]
    ) -> pd.DataFrame:
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
        (parsed_results, overall_result, stats) = self._parse_results_from_validator(
            validated_result
        )
        parsed_results = self.group_by_parsed_results_by_column(parsed_results)
        # print(f"\n\n\nparsed_results: {parsed_results}\n\n\n")
        final_df = self._make_df_with_is_good_col(parsed_results)
        return ValidatedResult(
            file_path=self.file_path,
            overall_result=overall_result,
            overall_statistics=stats,
            parsed_results_gx=parsed_results,
            docs_urls=docs_urls,
            final_df=final_df,
        )


def run_validate_data(file_path: str, batch_definition: str) -> ValidatedResult:
    validation_service = ValidationService(file_path, batch_definition)
    return validation_service.validate_data()

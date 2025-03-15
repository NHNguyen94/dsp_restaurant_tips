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
    GXResultBeOfTypeDetails,
    GXResultBetweenOrInSetDetails,
    OverallStatistics,
    AllResults,
    CSVResult,
    FailureMode,
    FailureModePerColumn,
)
from src.utils.configs_manager import QualityConfigs, DataConfigs
from src.utils.csv_parser import CSVParser
from src.utils.date_time_manager import DateTimeManager
from src.utils.helper import (
    find_numerical_values_in_df,
    find_non_numerical_values_in_df,
)

data_configs = DataConfigs()
quality_configs = QualityConfigs()


class ValidationService:
    def __init__(self, file_path: str, batch_definition: str):
        self.file_path = file_path
        self.batch_definition = batch_definition
        self.parser = CSVParser()
        self.df = self.parser.read_csv_from_file_path(self.file_path)
        self.df_after_validate_dtype = self.df.copy()
        self.expected_data = data_configs.EXPECTED_RESULTS_FOR_VALIDATION
        self.context = gx.get_context()
        self.default_delimiter = data_configs.DEFAULT_DELIMITER

    def _validate_csv(self) -> CSVResult:
        encoding = self.parser.validate_if_default_encoding(self.file_path)
        format = self.parser.validate_if_default_delimiter(self.file_path)
        if encoding and format:
            empty_file = self.parser.validate_if_empty_file(self.file_path)
        else:
            empty_file = None

        return CSVResult(
            encoding=encoding,
            format=format,
            empty_file=empty_file,
        )

    def _get_gx_batch(self, df: pd.DataFrame) -> Batch:
        data_source = self.context.data_sources.add_pandas(name="data")
        data_asset = data_source.add_dataframe_asset(name="pd DF asset")
        batch_def = data_asset.add_batch_definition_whole_dataframe(
            self.batch_definition
        )

        return batch_def.get_batch(batch_parameters={"dataframe": df})

    # https://github.com/great-expectations/great_expectations/blob/develop/tests/validator/test_validator.py
    def _get_gx_validator(self, df: pd.DataFrame) -> Validator:
        batch = self._get_gx_batch(df)

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
        validated_results_for_check_col_type: List[GXResultPerColumn] = None,
    ) -> (List[GXResultPerColumn], bool, OverallStatistics):
        parsed_results = []
        overall_result = input_results["success"]
        stats = OverallStatistics(**input_results["statistics"])

        results = input_results["results"]
        wrong_type_columns_to_ignore = []
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
                    **res["result"], result=res["success"]
                )
            if expectation_config["type"] == "expect_column_values_to_be_of_type":
                if res["success"] == False:
                    wrong_type_columns_to_ignore.append(
                        expectation_config["kwargs"]["column"]
                    )
                data_per_col.all_results.result_be_of_type = GXResultBeOfTypeDetails(
                    **res["result"], result=res["success"]
                )

            parsed_results.append(data_per_col)

        # Split to 2 for loops to validate the column first, then validate the value of the column
        for res in results:
            expectation_config = res["expectation_config"]
            data_per_col = GXResultPerColumn(
                success=res["success"],
                column=expectation_config["kwargs"]["column"],
                all_results=AllResults(),
            )
            if expectation_config["type"] in [
                "expect_column_values_to_be_in_set",
                "expect_column_values_to_be_between",
            ]:
                if (
                    expectation_config["kwargs"]["column"]
                    in wrong_type_columns_to_ignore
                ):
                    continue
                else:
                    # print(f"wrong_type_columns_to_ignore: {wrong_type_columns_to_ignore}")
                    # print(f"\n\n\nres: {res}\n\n\n")
                    data_per_col.all_results.result_between_or_in_set = (
                        GXResultBetweenOrInSetDetails(
                            **res["result"], result=res["success"]
                        )
                    )

            parsed_results.append(data_per_col)

        if validated_results_for_check_col_type:
            parsed_results.extend(validated_results_for_check_col_type)

        return (parsed_results, overall_result, stats)

    def _group_by_parsed_results_by_column(
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
                    if res.all_results.result_be_of_type:
                        new_all_res.result_be_of_type = (
                            res.all_results.result_be_of_type
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
            if data.all_results.result_column_exist == False and (
                data.all_results.result_not_null is None
                or data.all_results.result_be_of_type is None
                or data.all_results.result_between_or_in_set is None
            ):
                raise ValueError("Missing validation category")

        return grouped_results

    def validate_columns_with_validator(
        self,
    ) -> Union[ExpectationValidationResult, ExpectationSuiteValidationResult]:
        validator = self._get_gx_validator(self.df_after_validate_dtype)
        suite_name = "validation_suite"
        validator.expectation_suite_name = suite_name
        suite = self.context.suites.add(ExpectationSuite(suite_name))
        # print(f"\n\n\nself.expected_data: {self.expected_data}\n\n\n")
        for k, v in self.expected_data.items():
            expectation_col = gx.expectations.ExpectColumnToExist(column=k)
            suite.add_expectation(expectation_col)

            # Disabled since it's replace by the manual check in func validate_columns_dtype
            # The issue is that ExpectColumnValuesToBeOfType cannot recognize the case that the column has both number and string
            # Because pandas automatically converts the column to string => All the values are string and fail the validation
            # expectation_col_type = gx.expectations.ExpectColumnValuesToBeOfType(
            #     column=k, type_=v["type"]
            # )
            # suite.add_expectation(expectation_col_type)

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
                if (
                    res.all_results.result_column_exist == False
                ):  # Add on here for further error mode to remove all rows
                    remove_all_col = True
                    values_to_remove = []
                else:
                    remove_all_col = False
                    values_to_remove = (
                        res.all_results.result_not_null.partial_unexpected_list
                        + res.all_results.result_between_or_in_set.partial_unexpected_list
                        + res.all_results.result_be_of_type.partial_unexpected_list
                    )
                filter = {
                    "column": res.column,
                    "remove_all_rows": remove_all_col,
                    "values_to_remove": values_to_remove,
                }
                filter_conditions.append(filter)

        return filter_conditions

    def _make_df_with_is_good_col(
        self, parsed_results: List[GXResultPerColumn]
    ) -> pd.DataFrame:
        new_df = self.df.copy()
        filter_conditions = self._create_filter_conditions(parsed_results)
        # print(f"\n\n\nfilter_conditions: {filter_conditions}\n\n\n")
        if len(filter_conditions) > 0:
            new_df[quality_configs.IS_GOOD] = 1
            for filter in filter_conditions:
                if filter["remove_all_rows"]:
                    new_df[quality_configs.IS_GOOD] = 0
                else:
                    new_df.loc[
                        new_df[filter["column"]].isin(filter["values_to_remove"]),
                        quality_configs.IS_GOOD,
                    ] = 0
        else:
            new_df[quality_configs.IS_GOOD] = 1

        return new_df

    def _cast_dtype_df_after_check_dtype(self):
        for k, v in self.expected_data.items():
            if v["type"] in ["float", "int"]:
                self.df_after_validate_dtype[k] = pd.to_numeric(
                    self.df_after_validate_dtype[k],
                    errors="ignore",
                    # ignore to keep the NaN value for later validation
                )
            else:
                self.df_after_validate_dtype[k] = self.df_after_validate_dtype[
                    k
                ].astype(v["type"])

    def validate_columns_dtype(self) -> List[GXResultPerColumn]:
        validated_result_for_check_col_type = []
        for k, v in self.expected_data.items():
            element_count = self.df[k].count()
            if v["type"] in ["float", "int"]:
                partial_unexpected_list = find_non_numerical_values_in_df(self.df, k)
            elif v["type"] == "str":
                partial_unexpected_list = find_numerical_values_in_df(self.df, k)
            else:
                partial_unexpected_list = []
            unexpected_count = len(partial_unexpected_list)
            unexpected_percent = unexpected_count / element_count * 100
            if len(partial_unexpected_list) > 0:
                result = False
                self.df_after_validate_dtype = self.df_after_validate_dtype[
                    self.df_after_validate_dtype[k].isin(partial_unexpected_list)
                    == False
                ]
            else:
                result = True
            details = GXResultBeOfTypeDetails(
                result=result,
                element_count=element_count,
                unexpected_count=unexpected_count,
                unexpected_percent=unexpected_percent,
                partial_unexpected_list=list(set(partial_unexpected_list)),
            )
            validated_result_for_check_col_type.append(
                GXResultPerColumn(
                    success=result,
                    column=k,
                    all_results=AllResults(result_be_of_type=details),
                )
            )

        return validated_result_for_check_col_type

    def _parse_failure_modes(
        self, parsed_results: List[GXResultPerColumn]
    ) -> List[FailureModePerColumn]:
        failure_modes_all_columns = []
        for res in parsed_results:
            if res.success == False:
                if res.all_results.result_column_exist == False:
                    failure_mode = FailureMode(
                        failure_mode=QualityConfigs.COLUMN_NOT_EXIST,
                        count=1,
                    )
                    failure_modes_all_columns.append(
                        FailureModePerColumn(
                            column=res.column, failure_mode=failure_mode
                        )
                    )
                if res.all_results.result_not_null:
                    failure_mode = FailureMode(
                        failure_mode=QualityConfigs.NULL_VALUE,
                        count=res.all_results.result_not_null.unexpected_count,
                    )
                    failure_modes_all_columns.append(
                        FailureModePerColumn(
                            column=res.column, failure_mode=failure_mode
                        )
                    )
                if res.all_results.result_be_of_type:
                    failure_mode = FailureMode(
                        failure_mode=QualityConfigs.WRONG_DATA_TYPE,
                        count=res.all_results.result_be_of_type.unexpected_count,
                    )
                    failure_modes_all_columns.append(
                        FailureModePerColumn(
                            column=res.column, failure_mode=failure_mode
                        )
                    )
                if res.all_results.result_between_or_in_set:
                    failure_mode = FailureMode(
                        failure_mode=QualityConfigs.OUT_OF_RANGE,
                        count=res.all_results.result_between_or_in_set.unexpected_count,
                    )
                    failure_modes_all_columns.append(
                        FailureModePerColumn(
                            column=res.column, failure_mode=failure_mode
                        )
                    )

        return failure_modes_all_columns

    def _enrich_stats(
        self,
        stats: OverallStatistics,
        final_df: pd.DataFrame,
        parsed_results: List[GXResultPerColumn],
    ) -> OverallStatistics:
        failure_modes_all_columns = self._parse_failure_modes(parsed_results)
        rows_count = len(final_df)
        bad_rows_count = len(final_df[final_df[quality_configs.IS_GOOD] == 0])
        bad_rows_percent = bad_rows_count / rows_count * 100
        stats.rows_count = rows_count
        stats.bad_rows_count = bad_rows_count
        stats.bad_rows_percent = bad_rows_percent
        stats.failure_modes = failure_modes_all_columns

        return stats

    def validate_data(self) -> ValidatedResult:
        csv_result_validation = self._validate_csv()
        if (
            csv_result_validation.format == False
            or csv_result_validation.encoding == False
            or csv_result_validation.empty_file == True
        ):
            return ValidatedResult(
                file_path=self.file_path,
                overall_result=False,
                csv_results=csv_result_validation,
            )

        else:
            validated_result_for_check_col_type = self.validate_columns_dtype()
            self._cast_dtype_df_after_check_dtype()
            validated_result_no_check_col_type = self.validate_columns_with_validator()
            docs_urls = self._build_datadocs_urls(validated_result_no_check_col_type)
            (parsed_results, overall_result, stats) = (
                self._parse_results_from_validator(
                    validated_result_no_check_col_type,
                    validated_result_for_check_col_type,
                )
            )
            parsed_results = self._group_by_parsed_results_by_column(parsed_results)
            final_df = self._make_df_with_is_good_col(parsed_results)
            stats = self._enrich_stats(stats, final_df, parsed_results)
            return ValidatedResult(
                file_path=self.file_path,
                overall_result=overall_result,
                overall_statistics=stats,
                csv_results=csv_result_validation,
                parsed_results_gx=parsed_results,
                docs_urls=docs_urls,
                final_df=final_df,
            )


def run_validate_data(file_path: str, batch_definition: str) -> ValidatedResult:
    validation_service = ValidationService(file_path, batch_definition)

    return validation_service.validate_data()

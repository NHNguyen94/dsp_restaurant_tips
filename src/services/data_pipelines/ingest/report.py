from src.database.models import DataIssues
from src.database.service_manager import DatabaseServiceManager
from src.services.data_pipelines.models import ValidatedResult
from src.utils.configs_manager import QualityConfigs
from src.utils.date_time_manager import DateTimeManager

db_service_manager = DatabaseServiceManager()
quality_configs = QualityConfigs()


def _parse_validated_results_with_good_csv(
    validated_result: ValidatedResult,
) -> DataIssues:
    missing_columns = 0
    missing_values = 0
    duplicated_rows = 0
    unknown_categorical_values = 0
    unknown_numeric_values = 0
    total_rows = len(validated_result.final_df)
    total_bad_rows = len(
        validated_result.final_df[
            validated_result.final_df[f"{quality_configs.IS_GOOD}"] != 1
        ]
    )

    parsed_results_gx = validated_result.parsed_results_gx
    for res in parsed_results_gx:
        if res.success == False:
            all_res = res.all_results
            if all_res.result_column_exist == False:
                missing_columns += 1
            if all_res.result_not_null is not None:
                missing_values += 1
            if all_res.result_between_or_in_set is not None:
                if res.column in ["sex", "smoker", "day", "time"]:
                    unknown_categorical_values += (
                        all_res.result_between_or_in_set.unexpected_count
                    )
                if res.column in ["total_bill", "size"]:
                    unknown_numeric_values += (
                        all_res.result_between_or_in_set.unexpected_count
                    )

    # if there is a missing column => The whole dataset is invalid
    if missing_columns > 0:
        success_percent = 0
        unsuccessful_expectations = validated_result.overall_statistics.evaluated_expectations
        successful_expectations = 0
    else:
        success_percent = validated_result.overall_statistics.success_percent
        unsuccessful_expectations = validated_result.overall_statistics.unsuccessful_expectations
        successful_expectations = validated_result.overall_statistics.successful_expectations


    return DataIssues(
        file_path=validated_result.file_path,
        evaluated_expectations=validated_result.overall_statistics.evaluated_expectations,
        successful_expectations=successful_expectations,
        unsuccessful_expectations=unsuccessful_expectations,
        success_percent=success_percent,
        missing_columns=missing_columns,
        missing_values=missing_values,
        duplicated_rows=duplicated_rows,
        unknown_categorical_values=unknown_categorical_values,
        unknon_numeric_values=unknown_numeric_values,
        bad_csv_encoding=0,
        bad_csv_format=0,
        other_parse_issues=0,
        total_rows=total_rows,
        total_bad_rows=total_bad_rows,
        created_at=DateTimeManager.get_current_local_time(),
    )


def _parse_validated_results_with_bad_csv(
    validated_result: ValidatedResult,
) -> DataIssues:
    bad_csv_encoding = 0
    bad_csv_format = 0
    other_parse_issues = 0

    if validated_result.csv_results is not None:
        if validated_result.csv_results.good_encoding == False:
            bad_csv_encoding += 1
        if validated_result.csv_results.good_delimiter == False:
            bad_csv_format += 1
        if validated_result.csv_results.no_other_parse_issues == False:
            other_parse_issues += 1

    return DataIssues(
        file_path=validated_result.file_path,
        bad_csv_encoding=bad_csv_encoding,
        bad_csv_format=bad_csv_format,
        other_parse_issues=other_parse_issues,
        created_at=DateTimeManager.get_current_local_time(),
    )


def run_save_statistics(validated_result: ValidatedResult) -> None:
    if (
        validated_result.csv_results.good_encoding
        and validated_result.csv_results.good_delimiter
        and validated_result.csv_results.no_other_parse_issues
    ):
        data_issues = _parse_validated_results_with_good_csv(validated_result)
        db_service_manager.append_data_issues(data_issues)
    else:
        data_issues = _parse_validated_results_with_bad_csv(validated_result)
        db_service_manager.append_data_issues(data_issues)

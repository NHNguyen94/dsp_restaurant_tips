from src.database.models import DataIssues
from src.database.service_manager import DatabaseServiceManager
from src.services.data_pipelines.models import ValidatedResult
from src.utils.date_time_manager import DateTimeManager

db_service_manager = DatabaseServiceManager()


def _parse_validated_results_to_data_issues(
    validated_result: ValidatedResult,
) -> DataIssues:
    missing_columns = 0
    missing_values = 0
    duplicated_rows = 0
    unknown_categorical_values = 0
    unknon_numeric_values = 0
    bad_csv_encoding = 0
    bad_csv_format = 0

    if validated_result.csv_results is not None:
        if validated_result.csv_results.good_encoding:
            bad_csv_encoding += 1
        if validated_result.csv_results.good_delimiter:
            bad_csv_format += 1

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
                    unknon_numeric_values += (
                        all_res.result_between_or_in_set.unexpected_count
                    )

    return DataIssues(
        file_path=validated_result.file_path,
        evaluated_expectations=validated_result.overall_statistics.evaluated_expectations,
        successful_expectations=validated_result.overall_statistics.successful_expectations,
        unsuccessful_expectations=validated_result.overall_statistics.unsuccessful_expectations,
        success_percent=validated_result.overall_statistics.success_percent,
        missing_columns=missing_columns,
        missing_values=missing_values,
        duplicated_rows=duplicated_rows,
        unknown_categorical_values=unknown_categorical_values,
        unknon_numeric_values=unknon_numeric_values,
        bad_csv_encoding=bad_csv_encoding,
        bad_csv_format=bad_csv_format,
        created_at=DateTimeManager.get_current_local_time(),
    )


def run_save_statistics(validated_result: ValidatedResult) -> None:
    if (
        validated_result.csv_results.good_encoding
        and validated_result.csv_results.good_delimiter
        and validated_result.csv_results.no_other_parse_issues
    ):
        data_issues = _parse_validated_results_to_data_issues(validated_result)
        db_service_manager.append_data_issues(data_issues)
    else:
        # TODO: Handle empty csv file
        pass

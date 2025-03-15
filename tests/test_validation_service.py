from pprint import pprint

from src.services.data_pipelines.ingest.validation import ValidationService
from src.services.data_pipelines.models import ValidatedResult


class TestValidationService:
    failed_test_csv_path = "tests/resources/failed_test_tips.csv"
    failed_test_csv_path_2 = "tests/resources/failed_test_tips_2.csv"
    passed_test_csv_path = "tests/resources/test_tips.csv"

    def test_validate_columns_dtype(self):
        validation_service = ValidationService(
            self.failed_test_csv_path, "failed batch"
        )
        result = validation_service.validate_columns_dtype()
        # print(f"\nresult_validate_columns_dtype: {result}")

    def test_validate_columns_with_validator(self):
        validation_service = ValidationService(
            self.failed_test_csv_path, "failed batch"
        )
        result = validation_service.validate_columns_with_validator()
        # print(f"\nresult_validate_columns_with_validator: {result}")

    def test_fail_validate_data_1(self):
        validation_service = ValidationService(
            self.failed_test_csv_path, "failed batch"
        )
        result = validation_service.validate_data()
        # pprint(f"\nresult_failed_test_validate_data_1: {result}")
        df = result.final_df
        total_good_cols = df["is_good"].sum()
        assert isinstance(result, ValidatedResult)
        assert total_good_cols == 1

    def test_fail_validate_data_2(self):
        validation_service = ValidationService(
            self.failed_test_csv_path_2, "failed batch"
        )
        result = validation_service.validate_data()
        # pprint(f"\nresult_failed_test_validate_data_2: {result}")
        df = result.final_df
        total_good_cols = df["is_good"].sum()
        assert isinstance(result, ValidatedResult)
        assert total_good_cols == 10

    def test_pass_validate_data(self):
        validation_service = ValidationService(
            self.passed_test_csv_path, "passed batch"
        )
        result = validation_service.validate_data()
        # pprint(f"\nresult_passed_test_validate_data: {result}")
        df = result.final_df
        total_good_cols = df["is_good"].sum()
        assert isinstance(result, ValidatedResult)
        assert total_good_cols == 3

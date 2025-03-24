from pprint import pprint
import pytest
from src.services.data_pipelines.ingest.validation import ValidationService
from src.services.data_pipelines.models import ValidatedResult
from src.utils.configs_manager import QualityConfigs

quality_configs = QualityConfigs()


class TestValidationService:
    failed_test_csv_path = "tests/resources/failed_test_tips.csv"
    failed_test_csv_path_2 = "tests/resources/failed_test_tips_2.csv"
    passed_test_csv_path = "tests/resources/test_tips.csv"
    custom_delimiter_csv_path = "tests/resources/custom_delimiter.csv"
    empty_csv_path = "tests/resources/empty_csv.csv"
    empty_csv_with_header_path = "tests/resources/empty_csv_with_header.csv"
    combined_false_correct_csv_path = "tests/resources/false_data.csv"
    missing_col_csv_path = "tests/resources/missing_columns.csv"

    def test_validate_failed_csv(self):
        validation_service = ValidationService(
            self.failed_test_csv_path, "failed batch"
        )
        result = validation_service._validate_csv()
        assert result.good_encoding == True
        assert result.good_delimiter == True
        assert result.no_other_parse_issues == True

    def test_validate_bad_delimiter_csv(self):
        validation_service = ValidationService(
            self.custom_delimiter_csv_path, "failed delimiter batch"
        )
        result = validation_service._validate_csv()
        assert result.good_encoding == True
        assert result.good_delimiter == False
        assert result.no_other_parse_issues == True

    def test_validate_empty_csv(self):
        validation_service = ValidationService(self.empty_csv_path, "empty batch")
        result = validation_service._validate_csv()
        assert result.good_encoding == True
        assert result.good_delimiter == False
        assert result.no_other_parse_issues == False

    def test_validate_empty_csv_with_header(self):
        validation_service = ValidationService(
            self.empty_csv_with_header_path, "empty batch with header"
        )
        result = validation_service._validate_csv()
        assert result.good_encoding == True
        assert result.good_delimiter == True
        assert result.no_other_parse_issues == False

    def test_validate_good_csv(self):
        validation_service = ValidationService(self.passed_test_csv_path, "good batch")
        result = validation_service._validate_csv()
        assert result.good_encoding == True
        assert result.good_delimiter == True
        assert result.no_other_parse_issues == True

    def test_validate_columns_dtype_pass_batch(self):
        validation_service = ValidationService(self.passed_test_csv_path, "pass batch")
        result = validation_service.validate_columns_dtype()
        # pprint(f"\nresult_validate_columns_dtype: {result}")
        for res in result:
            assert res.success == True

    def test_validate_columns_dtype_failed_batch(self):
        validation_service = ValidationService(
            self.failed_test_csv_path, "failed batch"
        )
        result = validation_service.validate_columns_dtype()
        # pprint(f"\nresult_validate_columns_dtype: {result}")
        for res in result:
            assert res.success == True

    def test_validate_columns_with_validator_pass_batch(self):
        validation_service = ValidationService(self.passed_test_csv_path, "pass batch")
        result = validation_service.validate_columns_with_validator()
        # pprint(f"\nresult_validate_columns_with_validator: {result}")
        assert result.success == True

    def test_validate_columns_with_validator_failed_batch(self):
        validation_service = ValidationService(
            self.failed_test_csv_path, "failed batch"
        )
        result = validation_service.validate_columns_with_validator()
        # pprint(f"\nresult_validate_columns_with_validator: {result}")
        assert result.success == False

    def test_fail_validate_data_failed_batch_1(self):
        validation_service = ValidationService(
            self.failed_test_csv_path, "failed batch"
        )
        result = validation_service.validate_data()
        # pprint(f"\nresult_failed_test_validate_data_1: {result}")
        df = result.final_df
        total_good_cols = df[quality_configs.IS_GOOD].sum()
        assert isinstance(result, ValidatedResult)
        assert total_good_cols == 1

    def test_fail_validate_data_failed_batch_2(self):
        validation_service = ValidationService(
            self.failed_test_csv_path_2, "failed batch"
        )
        result = validation_service.validate_data()
        # pprint(f"\nresult_failed_test_validate_data_2: {result}")
        df = result.final_df
        total_good_cols = df[quality_configs.IS_GOOD].sum()
        assert isinstance(result, ValidatedResult)
        assert total_good_cols == 10

    def test_pass_validate_data_pass_batch(self):
        validation_service = ValidationService(self.passed_test_csv_path, "pass batch")
        result = validation_service.validate_data()
        # pprint(f"\nresult_passed_test_validate_data: {result}")
        df = result.final_df
        total_good_cols = df[quality_configs.IS_GOOD].sum()
        assert isinstance(result, ValidatedResult)
        assert total_good_cols == 3

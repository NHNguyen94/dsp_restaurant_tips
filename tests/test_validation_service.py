from src.services.data_pipelines.models import ValidatedResult
from src.services.data_pipelines.ingest.validation import ValidationService


class TestValidationService:
    failed_test_csv_path = "tests/resources/failed_test_tips.csv"

    def test_validate_columns_with_validator(self):
        validation_service = ValidationService(
            self.failed_test_csv_path, "failed batch"
        )
        result = validation_service.validate_columns_with_validator()
        # print(f"\nresult_test_validate_columns_with_validator: {result}")

    def test_validate_data(self):
        validation_service = ValidationService(
            self.failed_test_csv_path, "failed batch"
        )
        result = validation_service.validate_data()
        print(f"\nresult_test_validate_data: {result}")
        df = result.final_df
        total_good_cols = df["is_good"].sum()
        assert isinstance(result, ValidatedResult)
        assert total_good_cols == 1

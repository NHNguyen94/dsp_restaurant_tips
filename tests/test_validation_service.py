from src.services.data_pipelines.validation import ValidationService
from src.utils.csv_parser import CSVParser


class TestValidationService:
    test_csv_path = "tests/resources/test_tips.csv"
    failed_test_csv_path = "tests/resources/failed_test_tips.csv"
    parser = CSVParser()

    # def test_pass_validate(self):
    #     validation_service = ValidationService(self.test_csv_path, "pass batch")
    #     result = validation_service.validate_columns()
    #     for k, v in result.items():
    #         assert v["success"] == True
    #
    # def test_fail_validate(self):
    #     validation_service = ValidationService(
    #         self.failed_test_csv_path, "fail batch 1"
    #     )
    #     result = validation_service.validate_columns()
    #     failed_indices = validation_service.get_failed_indices(result)
    #     assert len(failed_indices) == 2

    # def test_add_is_good_column(self):
    #     validation_service = ValidationService(
    #         self.failed_test_csv_path, "fail batch 2"
    #     )
    #     new_df = validation_service.add_is_good_column()
    #     assert new_df["is_good"].sum() == 1

    def test_validate_columns_with_validator(self):
        validation_service = ValidationService(self.test_csv_path, "pass batch")
        result = validation_service.validate_columns_with_validator()
        print(f"\n results: {result}")
        # for k, v in result.items():
        #     assert v["success"] == True

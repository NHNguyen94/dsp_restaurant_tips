from src.services.data_pipelines.validation import ValidationService
from src.utils.csv_parser import CSVParser

class TestValidationService:
    test_csv_path = "tests/resources/test_tips.csv"
    parser = CSVParser()

    def test_validate(self):
        validation_service = ValidationService(self.test_csv_path)
        result = validation_service.validate_columns()
        print(f"\n\n\n{result}\n\n\n")
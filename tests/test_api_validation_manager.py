from src.api.v1.models.prediction_request import PredictionRequest
from src.utils.api_validation_manager import APIValidationManager


class TestAPIValidationManager:
    def test_validate_none_json_request(self):
        none_request = PredictionRequest(
            total_bill=None, sex=None, smoker=None, day=None, time=None, size=None
        )
        assert APIValidationManager.validate_none_json_request(none_request) == True

        non_none_request = PredictionRequest(
            total_bill=10.0, sex=None, smoker=None, day=None, time=None, size=None
        )
        assert APIValidationManager.validate_none_json_request(non_none_request) == False

from typing import Dict, List

from src.database.models import Predictions
from src.database.service_manager import DatabaseServiceManager
from src.services.api_controller import ApiController
from src.utils.api_response_parser import ApiResponseParser
from src.utils.date_time_manager import DateTimeManager

api_controller = ApiController()
db_service_manager = DatabaseServiceManager()
api_response_parser = ApiResponseParser()


#
# async def _async_predict(file_path: List[str]) -> List[Dict]:
#     tasks = [api_controller.async_predict_with_file(file) for file in file_path]
#     return await asyncio.gather(*tasks)


def _parse_response(
    response: List[Dict], file_path: str, prediction_source: str
) -> List[Predictions]:
    print(f"Response: {response}")
    api_response = api_response_parser.parse_response(response)
    for res in api_response:
        res.prediction_source = prediction_source
        res.file_path = file_path
        res.predicted_at = DateTimeManager.get_current_local_time()
    print(f"Parsed response: {api_response}")
    return api_response


def run_predict_single_file(
    file_path: str, prediction_source: str
) -> List[Predictions]:
    response = api_controller.predict_with_file_content(file_path, prediction_source)

    return _parse_response(response, file_path, prediction_source)


#
# async def async_run_prediction(file_paths: List[str]) -> None:
#     response = await _async_predict(file_paths)
#     predictions = _parse_response(response)
#     await db_service_manager.async_append_predictions(predictions)


def run_predictions(file_paths: List[str], prediction_source: str) -> None:
    for file_path in file_paths:
        predictions = run_predict_single_file(
            file_path, prediction_source=prediction_source
        )
        # print(f"Predict :{len(predictions)} rows")
        # db_service_manager.append_predictions(predictions)

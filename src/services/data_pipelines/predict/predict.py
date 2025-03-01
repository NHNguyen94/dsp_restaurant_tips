import logging
from typing import Dict, List

from src.database.models import Predictions
from src.database.service_manager import DatabaseServiceManager
from src.services.api_controller import ApiController
from src.utils.api_response_parser import ApiResponseParser

api_controller = ApiController()
db_service_manager = DatabaseServiceManager()
api_response_parser = ApiResponseParser()


#
# async def _async_predict(file_path: List[str]) -> List[Dict]:
#     tasks = [api_controller.async_predict_with_file(file) for file in file_path]
#     return await asyncio.gather(*tasks)


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
def _parse_response(response: List[Dict], file_path: str) -> List[Predictions]:
    api_response = api_response_parser.parse_response(response)
=======
=======
>>>>>>> main
=======
>>>>>>> main
def _parse_response(
    response: List[Dict], file_path: str, prediction_source: str
) -> List[Predictions]:
    api_response = api_response_parser.parse_response(
        response, prediction_source=prediction_source
    )
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> main
=======
>>>>>>> main
=======
>>>>>>> main
    for res in api_response:
        res.file_path = file_path
    return api_response


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
def run_predict_single_file(file_path: str) -> List[Predictions]:
    response = api_controller.predict_with_file_manual_request(file_path)
    return _parse_response(response, file_path)
=======
=======
>>>>>>> main
=======
>>>>>>> main
def run_predict_single_file(
    file_path: str, prediction_source: str
) -> List[Predictions]:
    response = api_controller.predict_with_file_manual_request(file_path, prediction_source)
    return _parse_response(response, file_path, prediction_source)
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> main
=======
>>>>>>> main
=======
>>>>>>> main


#
# async def async_run_prediction(file_paths: List[str]) -> None:
#     response = await _async_predict(file_paths)
#     predictions = _parse_response(response)
#     await db_service_manager.async_append_predictions(predictions)


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
def run_predictions(file_paths: List[str]) -> None:
    for file_path in file_paths:
        predictions = run_predict_single_file(file_path)
        logging.warning(f"Predictions: {predictions} for file: {file_path}")
        db_service_manager.append_predictions(predictions)
=======
=======
>>>>>>> main
=======
>>>>>>> main
def run_predictions(file_paths: List[str], prediction_source: str) -> None:
    for file_path in file_paths:
        predictions = run_predict_single_file(
            file_path, prediction_source=prediction_source
        )
        # db_service_manager.append_predictions(predictions)
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> main
=======
>>>>>>> main
=======
>>>>>>> main

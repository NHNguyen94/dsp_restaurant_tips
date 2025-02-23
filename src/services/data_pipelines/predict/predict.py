import asyncio
from typing import Dict, List

from src.database.models import Predictions
from src.database.service_manager import DatabaseServiceManager
from src.services.api_controller import ApiController
from src.utils.api_response_parser import ApiResponseParser

api_controller = ApiController()
db_service_manager = DatabaseServiceManager()
api_response_parser = ApiResponseParser()


async def _predict(file_path: List[str]) -> List[Dict]:
    tasks = [api_controller.async_predict_with_file(file) for file in file_path]
    return await asyncio.gather(*tasks)


def _parse_response(response: List[Dict]) -> List[Predictions]:
    return api_response_parser.parse_response(response)


async def run_prediction(file_paths: List[str]) -> None:
    response = await _predict(file_paths)
    predictions = _parse_response(response)
    await db_service_manager.async_append_predictions(predictions)

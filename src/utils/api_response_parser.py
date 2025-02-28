from typing import Dict, List

from src.database.models import Predictions
from src.utils import DateTimeManager


class ApiResponseParser:
    def __init__(self):
        pass

    @staticmethod
    def parse_response(
        response: List[Dict], prediction_source: str
    ) -> List[Predictions]:
        return [
            Predictions(
                **res,
                prediction_source=prediction_source,
                created_at=DateTimeManager.get_current_local_time(),
            )
            for res in response
        ]

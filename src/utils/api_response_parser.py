from typing import Dict, List

from src.database.models import Predictions
from src.utils import DateTimeManager


class ApiResponseParser:
    def __init__(self):
        pass

    @staticmethod
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    def parse_response(response: List[Dict]) -> List[Predictions]:
        return [
            Predictions(**res, created_at=DateTimeManager.get_current_local_time())
=======
=======
>>>>>>> main
=======
>>>>>>> main
    def parse_response(
        response: List[Dict], prediction_source: str
    ) -> List[Predictions]:
        return [
            Predictions(
                **res,
                prediction_source=prediction_source,
                predicted_at=DateTimeManager.get_current_local_time(),
            )
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> main
=======
>>>>>>> main
=======
>>>>>>> main
            for res in response
        ]

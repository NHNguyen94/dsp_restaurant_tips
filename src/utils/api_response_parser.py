from typing import Dict, List

from src.database.models import Predictions


class ApiResponseParser:
    def __init__(self):
        pass

    @staticmethod
    def parse_response(response: List[Dict]) -> List[Predictions]:
        return [Predictions(**res) for res in response]

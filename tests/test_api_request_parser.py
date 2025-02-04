import pytest
from fastapi import UploadFile

from src.api.v1.models import PredictionRequest
from src.utils.api_request_parser import ApiRequestParser


class TestApiRequestParser:
    test_csv_path = "tests/resources/test_tips.csv"
    parser = ApiRequestParser()

    @pytest.mark.asyncio
    async def test_parse_single_csv_to_request(self):
        with open(self.test_csv_path, "rb") as f:
            file = UploadFile(f)
            requests = await self.parser.parse_single_csv_to_request(file)
            assert len(requests) == 3
            assert isinstance(requests[0], PredictionRequest)

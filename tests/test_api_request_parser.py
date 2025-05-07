import pytest
from fastapi import UploadFile

from src.api.v1.models import PredictionRequest
from src.utils.api_request_parser import ApiRequestParser


class TestApiRequestParser:
    test_csv_path = "tests/resources/test_tips.csv"
    parser = ApiRequestParser()
    selected_columns = ["total_bill", "sex", "smoker", "day", "time", "size"]

    @pytest.mark.asyncio
    async def test_parse_single_csv_to_request(self):
        with open(self.test_csv_path, "rb") as f:
            file = UploadFile(f)
            requests = await self.parser.parse_single_csv_to_request(file)
            assert len(requests) == 3
            assert isinstance(requests[0], PredictionRequest)

    @pytest.mark.asyncio
    async def test_parse_csv_to_df(self):
        with open(self.test_csv_path, "rb") as f:
            file = UploadFile(f)
            df = await self.parser.parse_csv_to_df(file)
            assert list(df.columns) == self.selected_columns
            assert len(df) == 3

    def test_get_fields(self):
        columns = self.parser._get_fields()
        assert columns == self.selected_columns

    def test_parse_request_to_df(self):
        request = PredictionRequest(
            total_bill=16.99, sex="Male", smoker="No", day="Sun", time="Dinner", size=2
        )
        df = self.parser.parse_request_to_df(request)
        assert len(df) == 1

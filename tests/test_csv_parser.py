import pytest
from fastapi import UploadFile

from src.utils.csv_parser import CSVParser


@pytest.mark.asyncio
class TestCsvParser:
    test_csv_path = "tests/resources/test_tips.csv"
    paser = CSVParser()

    async def test_read_csv_from_file_upload(self):
        with open(self.test_csv_path, "rb") as f:
            file = UploadFile(f)
            df = await self.paser.read_csv_from_file_upload(file)
            assert df.columns.tolist() == ["total_bill", "tip", "sex", "smoker", "day", "time", "size"]
            assert df.shape == (3, 7)

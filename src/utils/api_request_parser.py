from typing import List

from fastapi import HTTPException, UploadFile

from src.api.v1.models import PredictionRequest
from src.utils.csv_parser import CSVParser


class ApiRequestParser:
    def __init__(self):
        self.csv_parser = CSVParser()

    async def parse_single_csv_to_request(
        self, input_csv: UploadFile
    ) -> List[PredictionRequest]:
        try:
            df = await self.csv_parser.read_csv_from_file_upload(input_csv)
            return [PredictionRequest(**row) for row in df.to_dict(orient="records")]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid CSV file: {e}")

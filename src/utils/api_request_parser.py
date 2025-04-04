from io import StringIO
from typing import List

import pandas as pd
from fastapi import HTTPException, UploadFile

from src.api.v1.models import PredictionRequest
from src.utils.csv_parser import CSVParser


class ApiRequestParser:
    def __init__(self):
        self.csv_parser = CSVParser()

    def _get_fields(self) -> List[str]:
        return list(PredictionRequest.__fields__.keys())

    def _limit_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[self._get_fields()]

    async def parse_single_csv_to_request(
            self, input_csv: UploadFile
    ) -> List[PredictionRequest]:
        try:
            df = await self.csv_parser.read_csv_from_file_upload(input_csv)
            return [PredictionRequest(**row) for row in df.to_dict(orient="records")]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid CSV file: {e}")

    def parse_request_to_df(self, request: PredictionRequest) -> pd.DataFrame:
        df = pd.DataFrame([request.dict()])
        return self._limit_columns(df)

    async def parse_csv_to_df(self, input_csv: UploadFile) -> pd.DataFrame:
        df = await self.csv_parser.read_csv_from_file_upload(input_csv)
        return self._limit_columns(df)

    async def read_file_content_to_df(self, file_content: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(StringIO(file_content))
            return self._limit_columns(df)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid file content: {e}")

import io

import chardet
import pandas as pd
from fastapi import UploadFile

from src.utils.configs_manager import DataConfigs


class CSVParser:
    def __init__(self):
        self.decoder = DataConfigs.DEFAULT_DECODER
        self.accepted_encodings = DataConfigs.ACCEPTED_ENCODINGS
        self.default_delimiter = DataConfigs.DEFAULT_DELIMITER

    async def read_csv_from_file_upload(
        self, file: UploadFile, delimiter: str = None
    ) -> pd.DataFrame:
        if delimiter is None:
            delimiter = self.default_delimiter
        contents = await file.read()
        return pd.read_csv(
            io.StringIO(contents.decode(self.decoder)), delimiter=delimiter
        )

    def read_csv_from_file_path(
        self, file_path: str, delimiter: str = None
    ) -> pd.DataFrame:
        if delimiter is None:
            delimiter = self.default_delimiter
        return pd.read_csv(file_path, delimiter=delimiter, encoding=self.decoder)

    def validate_if_default_delimiter(self, file_path: str) -> bool:
        with open(file_path, "r") as file:
            first_line = file.readline()
            if self.default_delimiter in first_line:
                return True
            return False

    # https://www.geeksforgeeks.org/detect-encoding-of-csv-file-in-python/
    def validate_if_default_encoding(self, file_path: str) -> bool:
        try:
            with open(file_path, "rb") as file:
                rawdata = file.read()
            encode = chardet.detect(rawdata)
            if encode["encoding"] in self.accepted_encodings:
                return True
            return False
        except Exception:
            return False

    def validate_if_can_parse(self, file_path: str) -> bool:
        try:
            df = self.read_csv_from_file_path(file_path)
            if df.empty:
                return False
            return True
        except Exception:
            return False

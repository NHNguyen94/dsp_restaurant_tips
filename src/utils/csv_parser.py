import io

import pandas as pd
from fastapi import UploadFile


class CSVParser:
    def __init__(self):
        self.decoder = "utf-8"
        self.default_delimiter = ","

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
        return pd.read_csv(file_path, delimiter=delimiter)

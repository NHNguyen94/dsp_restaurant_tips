import io

import pandas as pd
from fastapi import UploadFile


class CSVParser:
    def __init__(self):
        self.decoder = "utf-8"

    async def read_csv_from_file_upload(self, file: UploadFile) -> pd.DataFrame:
        contents = await file.read()
        return pd.read_csv(io.StringIO(contents.decode(self.decoder)))

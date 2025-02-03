import io

import pandas as pd
from fastapi import UploadFile


class CSVParser():

    def __init__(self):
        pass

    async def read_csv_from_file_upload(self, file: UploadFile) -> pd.DataFrame:
        contents = await file.read()
        return pd.read_csv(io.StringIO(contents.decode("utf-8")))

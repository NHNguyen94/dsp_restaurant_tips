from pydantic import BaseModel


class Anomaly(BaseModel):
    total_null: int
    total_missing_columns: int
    total_wrong_dtype: int
    total_wrong_format: int
    total_not_accept_value: int


class BadData(BaseModel):
    file_path: str
    anomaly: Anomaly

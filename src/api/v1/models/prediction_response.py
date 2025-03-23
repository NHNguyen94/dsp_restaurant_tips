from typing import List

from pydantic import BaseModel


class PredictionResponse(BaseModel):
    total_bill: float
    sex: str
    smoker: bool
    day: str
    time: str
    size: int
    tip: float
    predicted_at: str
    prediction_source: str
    file_path: str = None


class PredictionResponseDataFrame(BaseModel):
    columns: List[str]
    data: List[List]

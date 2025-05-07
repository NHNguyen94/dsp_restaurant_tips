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
    predicted_at: str = None
    prediction_source: str = None
    file_path: str = None


class PredictionResponseDataFrame(BaseModel):
    columns: List[str]
    data: List[List]

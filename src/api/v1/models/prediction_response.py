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

class PredictionResponseDataFrame(BaseModel):
    columns: List[str]
    data: List[List]

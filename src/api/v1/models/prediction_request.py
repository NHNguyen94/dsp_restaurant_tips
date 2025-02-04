from pydantic import BaseModel


class PredictionRequest(BaseModel):
    total_bill: float
    sex: str
    smoker: bool
    day: str
    time: str
    size: int

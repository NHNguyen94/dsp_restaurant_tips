from pydantic import BaseModel


class PredictionResponse(BaseModel):
    tip: float

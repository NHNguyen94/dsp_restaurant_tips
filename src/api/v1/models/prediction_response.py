from pydantic import BaseModel


class PredictionResponse(BaseModel):
    quantity: int

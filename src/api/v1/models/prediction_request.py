from typing import Literal

from pydantic import BaseModel, model_validator

from fastapi import HTTPException


class PredictionRequest(BaseModel):
    total_bill: float
    sex: Literal["Male", "Female"]
    smoker: Literal["Yes", "No"]
    day: Literal["Sun", "Sat", "Fri", "Thur", "Wed", "Tue", "Mon"]
    time: Literal["Lunch", "Dinner"]
    size: int

    # Ref: https://docs.pydantic.dev/latest/api/functional_validators/#pydantic.functional_validators.model_validator
    @model_validator(mode="after")
    def validate_numbers(self):
        if self.total_bill <= 0:
            raise HTTPException(
                status_code=400, detail="total_bill must be greater than 0."
            )
        if self.size <= 0:
            raise HTTPException(status_code=400, detail="size must be greater than 0.")
        return self

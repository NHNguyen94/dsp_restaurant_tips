from typing import Literal, Optional

from pydantic import BaseModel, model_validator

from fastapi import HTTPException

class PredictionRequest(BaseModel):
    total_bill: Optional[float] = None
    sex: Optional[Literal["Male", "Female"]] = None
    smoker: Optional[Literal["Yes", "No"]] = None
    day: Optional[Literal["Sun", "Sat", "Fri", "Thur", "Wed", "Tue", "Mon"]] = None
    time: Optional[Literal["Lunch", "Dinner"]] = None
    size: Optional[int] = None

    # Ref: https://docs.pydantic.dev/latest/api/functional_validators/#pydantic.functional_validators.model_validator
    @model_validator(mode="after")
    def validate_numbers(self):
        if self.total_bill is not None and self.size is not None:
            if self.total_bill <= 0:
                raise HTTPException(
                    status_code=400, detail="total_bill must be greater than 0."
                )
            if self.size <= 0:
                raise HTTPException(status_code=400, detail="size must be greater than 0.")
        return self
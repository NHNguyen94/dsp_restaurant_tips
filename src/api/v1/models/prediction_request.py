from typing import Literal, Optional
from src.utils.date_time_manager import DateTimeManager
from pydantic import BaseModel, validator


class PastPredictionRequest(BaseModel):
    start_date: str
    end_date: str
    prediction_source: Literal["webapp", "scheduled_predictions", "all"] = "all"

    @validator("start_date")
    def start_date_must_be_valid(cls, v):
        try:
            DateTimeManager.parse_str_to_date(v)
        except:
            raise ValueError("start_date must be in the format YYYY-MM-DD")
        return v

    @validator("end_date")
    def end_date_must_be_valid(cls, v):
        try:
            DateTimeManager.parse_str_to_date(v)
        except:
            raise ValueError("end_date must be in the format YYYY-MM-DD")
        return v


class PredictionRequest(BaseModel):
    total_bill: Optional[float] = None
    sex: Optional[Literal["Male", "Female"]] = None
    smoker: Optional[Literal["Yes", "No"]] = None
    day: Optional[Literal["Sun", "Sat", "Fri", "Thur", "Wed", "Tue", "Mon"]] = None
    time: Optional[Literal["Lunch", "Dinner"]] = None
    size: Optional[int] = None

    # https://docs.pydantic.dev/1.10/usage/validators/
    @validator("total_bill")
    def total_bill_must_be_positive(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("total_bill must be positive")
            return v

    @validator("size")
    def size_must_be_positive(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("size must be positive")
            return v

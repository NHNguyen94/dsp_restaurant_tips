from typing import Optional

import pandas as pd
from fastapi import APIRouter, UploadFile, File

from src.api.v1.models import PredictionRequest, PredictionResponseDataFrame

router = APIRouter(tags=["prediction"])


@router.post("/predict", response_model=PredictionResponseDataFrame)
async def predict(
        request: Optional[PredictionRequest] = None,
        input_files: Optional[UploadFile] = File(None)
):
    df = pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["A", "B", "C"]
    })
    return PredictionResponseDataFrame(columns=df.columns.tolist(), data=df.values.tolist())


@router.post("/past-predictions", response_model=PredictionResponseDataFrame)
async def past_predictions(request: PredictionRequest):
    df = pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["A", "B", "C"]
    })
    return PredictionResponseDataFrame(columns=df.columns.tolist(), data=df.values.tolist())

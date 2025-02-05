from typing import List, Optional

from fastapi import APIRouter, UploadFile, File

from src.api.v1.models import PredictionRequest, PredictionResponse

router = APIRouter(tags=["prediction"])


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    request_body: Optional[PredictionRequest] = None,
    input_files: UploadFile = File(None),
):
    pass


@router.post("/past-predictions", response_model=PredictionResponse)
async def past_predictions(request: PredictionRequest):
    pass

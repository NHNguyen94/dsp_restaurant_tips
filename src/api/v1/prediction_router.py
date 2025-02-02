from fastapi import APIRouter

from src.api.v1.models import PredictionRequest, PredictionResponse

router = APIRouter(tags=["prediction"])


@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    pass


@router.post("/past-predictions", response_model=PredictionResponse)
def past_predictions(request: PredictionRequest):
    pass

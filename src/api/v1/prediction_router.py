from typing import List, Annotated

from fastapi import APIRouter, UploadFile, File, Depends

from src.api.v1.models import PredictionRequest, PredictionResponse
from src.database.models import Predictions
from src.database.service_manager import DatabaseServiceManager
from src.services.ml_pipelines.inference import async_predict_response_with_features
from src.utils.api_request_parser import ApiRequestParser
from src.utils.validation_manager import ValidationManager

router = APIRouter(tags=["prediction"])

api_request_parser = ApiRequestParser()
db_service_manager = DatabaseServiceManager()


def _parse_predictions_to_api_response(
    predictions: List[Predictions],
) -> List[PredictionResponse]:
    responses = []
    for (prediction,) in predictions:
        res = PredictionResponse(
            total_bill=prediction.total_bill,
            sex=prediction.sex,
            smoker=bool(prediction.smoker),
            day=prediction.day,
            time=prediction.time,
            size=prediction.size,
            tip=prediction.tip,
        )
        responses.append(res)
    return responses


@router.post("/predict", response_model=List[PredictionResponse])
async def predict(
    input_json: Annotated[PredictionRequest, Depends()] = None,
    input_file: Annotated[UploadFile, File()] = None,
):
    if ValidationManager.validate_none_json_request(input_json) == False:
        df = api_request_parser.parse_request_to_df(input_json)
    elif input_file:
        df = await api_request_parser.parse_csv_to_df(input_file)
    else:
        raise ValueError("Either request body or input file must be provided.")

    df_with_predictions = await async_predict_response_with_features(df)
    return df_with_predictions.to_dict(orient="records")


@router.post("/past-predictions", response_model=List[PredictionResponse])
async def past_predictions(date: str):
    predicted_results = db_service_manager.get_predicted_results_by_date(date)
    print(f"predicted_results: {predicted_results[:3]}")
    return _parse_predictions_to_api_response(predicted_results)

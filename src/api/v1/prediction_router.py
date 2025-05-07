from typing import List, Annotated, Literal

from fastapi import APIRouter, Depends, Body

from src.api.v1.models import (
    PredictionRequest,
    PredictionResponse,
    PastPredictionRequest,
)
from src.database.models import Predictions
from src.database.service_manager import DatabaseServiceManager
from src.services.ml_pipelines.inference import async_predict_response_with_features
from src.utils import DateTimeManager
from src.utils.api_request_parser import ApiRequestParser
from src.utils.api_validation_manager import APIValidationManager

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
            predicted_at=DateTimeManager.parse_datetime_to_str(prediction.predicted_at),
            prediction_source=prediction.prediction_source,
            file_path=prediction.file_path,
        )
        responses.append(res)

    return responses


@router.post("/predict", response_model=List[PredictionResponse])
async def predict(
    input_json: Annotated[PredictionRequest, Depends()] = None,
    input_file: str = Body(default=None, media_type="text/csv"),
    # file_path is to save the file to the database, not to read data from it
    file_path: str = None,
    prediction_source: Literal["webapp", "scheduled_predictions"] = "webapp",
):
    if APIValidationManager.validate_none_json_request(input_json) == False:
        df = api_request_parser.parse_request_to_df(input_json)
    elif input_file:
        df = await api_request_parser.read_file_content_to_df(input_file)
    else:
        raise ValueError("Either request body or input file must be provided.")

    df_with_predictions = await async_predict_response_with_features(df)
    db_service_manager.append_df_to_predictions(
        df_with_predictions, file_path, prediction_source
    )

    return df_with_predictions.to_dict(orient="records")


@router.post("/past-predictions", response_model=List[PredictionResponse])
async def past_predictions(request: Annotated[PastPredictionRequest, Depends()]):
    predicted_results = db_service_manager.get_predicted_results_by_date_range(
        request.start_date, request.end_date, request.prediction_source
    )

    return _parse_predictions_to_api_response(predicted_results)

from typing import List, Annotated

from fastapi import APIRouter, UploadFile, File, Depends

from src.api.v1.models import PredictionRequest, PredictionResponse
from src.ml_pipelines.inference import async_predict_response_with_features
from src.utils.api_request_parser import ApiRequestParser

router = APIRouter(tags=["prediction"])

api_request_parser = ApiRequestParser()


@router.post("/predict", response_model=List[PredictionResponse])
async def predict(
        input_json: Annotated[PredictionRequest, Depends()] = None,
        input_file: Annotated[UploadFile, File()] = None
):
    if input_json != None:
        df = api_request_parser.parse_request_to_df(input_json)
    elif input_file != None:
        df = await api_request_parser.parse_csv_to_df(input_file)
    else:
        raise ValueError("Either request body or input file must be provided.")

    df_with_predictions = await async_predict_response_with_features(df)
    print(df_with_predictions)
    print(df_with_predictions.to_dict(orient="records"))
    return df_with_predictions.to_dict(orient="records")


@router.post("/past-predictions", response_model=PredictionResponse)
async def past_predictions():
    pass

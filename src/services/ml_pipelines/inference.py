import asyncio

import joblib
import numpy as np
import pandas as pd
from xgboost import Booster, DMatrix, XGBRegressor

from src.services.ml_pipelines.pre_processing import process_data
from src.utils.configs_manager import ModelPathConfigs, ModelConfigs
from src.utils.helper import round_number

model_path_configs = ModelPathConfigs.get_configs()
model_configs = ModelConfigs()


def _load_model() -> Booster:
    model = Booster()
    model.load_model(model_path_configs.MODEL_PATH)
    return model


def _load_model_by_joblib() -> XGBRegressor:
    model = joblib.load(model_path_configs.MODEL_PATH)
    return model

def predict(df: pd.DataFrame) -> np.ndarray:
    # model = _load_model()
    # dmatrix = DMatrix(df)
    # predictions = model.predict(dmatrix)
    model = _load_model_by_joblib()
    predictions = model.predict(df)
    predictions = np.array([round_number(pred) for pred in predictions])
    return predictions


def predict_response_with_features(df: pd.DataFrame) -> pd.DataFrame:
    processed_df = process_data(df)
    predictions = predict(processed_df)
    new_df = df.copy()
    new_df[model_configs.TIP] = predictions
    return new_df


async def async_predict(df: pd.DataFrame) -> np.ndarray:
    # model = _load_model()
    # dmatrix = DMatrix(df)
    model = _load_model_by_joblib()
    loop = asyncio.get_running_loop()
    predictions = await loop.run_in_executor(None, model.predict, df)
    predictions = np.array([round_number(pred) for pred in predictions])
    return predictions


async def async_predict_response_with_features(df: pd.DataFrame) -> pd.DataFrame:
    processed_df = process_data(df)
    predictions = await async_predict(processed_df)
    new_df = df.copy()
    new_df[model_configs.TIP] = predictions
    return new_df

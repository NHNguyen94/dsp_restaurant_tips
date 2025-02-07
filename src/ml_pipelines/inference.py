import asyncio

import numpy as np
import pandas as pd
from xgboost import Booster, DMatrix

from src.utils.configs_manager import ModelPathConfigs

model_path_configs = ModelPathConfigs.get_configs()


def _load_model() -> Booster:
    model = Booster()
    model.load_model(model_path_configs.MODEL_PATH)
    return model


def predict(df: pd.DataFrame) -> np.ndarray:
    model = _load_model()
    dmatrix = DMatrix(df)
    predictions = model.predict(dmatrix)
    return predictions


async def async_predict(df: pd.DataFrame) -> np.ndarray:
    model = _load_model()
    dmatrix = DMatrix(df)
    predictions = await asyncio.to_thread(model.predict, dmatrix)

    return predictions

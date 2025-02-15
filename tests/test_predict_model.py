import pandas as pd
import pytest

from src.services.ml_pipelines import (
    async_predict,
    async_predict_response_with_features,
)
from src.services.ml_pipelines import process_data
from src.utils.configs_manager import ModelPathConfigs, ModelConfigs

model_path_configs = ModelPathConfigs.get_configs()
model_configs = ModelConfigs()


class TestPredictModel:
    @pytest.mark.asyncio
    async def test_async_predict_model(self):
        df = pd.read_csv(model_path_configs.TEST_DATA_PATH)
        df = df.drop(columns=[model_configs.TIP])
        processed_df = process_data(df)
        predictions = await async_predict(processed_df)
        assert len(predictions) == len(processed_df)

    @pytest.mark.asyncio
    async def test_async_predict_response_with_features(self):
        df = pd.read_csv(model_path_configs.TEST_DATA_PATH)
        df = df.drop(columns=[model_configs.TIP])
        df_with_predictions = await async_predict_response_with_features(df)
        print(df_with_predictions)
        assert df_with_predictions[model_configs.TIP] is not None
        assert len(df_with_predictions) == len(df)

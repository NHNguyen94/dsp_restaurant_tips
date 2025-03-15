import pandas as pd
import pytest

from src.services.ml_pipelines.inference import (
    predict,
    predict_response_with_features,
    async_predict,
    async_predict_response_with_features,
)
from src.services.ml_pipelines.pre_processing import process_data
from src.utils.configs_manager import ModelConfigs

model_configs = ModelConfigs()


class TestPredictModel:
    test_data_path = "tests/resources/test_tips.csv"

    def test_predict_model(self):
        df = pd.read_csv(self.test_data_path)
        df = df.drop(columns=[model_configs.TIP])
        processed_df = process_data(df)
        predictions = predict(processed_df)
        assert len(predictions) == len(processed_df)

    def test_predict_response_with_features(self):
        df = pd.read_csv(self.test_data_path)
        df = df.drop(columns=[model_configs.TIP])
        df_with_predictions = predict_response_with_features(df)
        assert df_with_predictions[model_configs.TIP] is not None
        assert len(df_with_predictions) == len(df)

    @pytest.mark.asyncio
    async def test_async_predict_model(self):
        df = pd.read_csv(self.test_data_path)
        df = df.drop(columns=[model_configs.TIP])
        processed_df = process_data(df)
        predictions = await async_predict(processed_df)
        assert len(predictions) == len(processed_df)

    @pytest.mark.asyncio
    async def test_async_predict_response_with_features(self):
        df = pd.read_csv(self.test_data_path)
        df = df.drop(columns=[model_configs.TIP])
        df_with_predictions = await async_predict_response_with_features(df)
        assert df_with_predictions[model_configs.TIP] is not None
        assert len(df_with_predictions) == len(df)

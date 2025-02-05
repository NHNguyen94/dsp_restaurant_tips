import pandas as pd

from src.ml_pipelines.inference import predict
from src.ml_pipelines.pre_processing import process_data
from src.utils.configs_manager import ModelPathConfigs

model_path_configs = ModelPathConfigs.get_configs()


class TestPredictModel:

    def test_predict_model(self):
        df = pd.read_csv(model_path_configs.TEST_DATA_PATH)

        df = df.drop(columns=["tip"])
        processed_df = process_data(df)
        predictions = predict(processed_df)
        processed_df["tip"] = predictions
        assert processed_df["tip"] is not None
        assert len(processed_df) == len(df)

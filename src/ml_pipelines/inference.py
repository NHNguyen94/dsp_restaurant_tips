import numpy as np
import pandas as pd
from xgboost import Booster, DMatrix

from src.ml_pipelines.pre_processing import process_data
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


def main():
    df = pd.read_csv(model_path_configs.TEST_DATA_PATH)
    df = df.drop(columns=["tip"])
    processed_df = process_data(df)
    predictions = predict(processed_df)
    processed_df["tip"] = predictions
    print(processed_df)


if __name__ == "__main__":
    main()

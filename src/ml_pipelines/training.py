import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

from src.utils.configs_manager import ModelPathConfigs, ModelConfigs

model_path_configs = ModelPathConfigs.get_configs()
model_configs = ModelConfigs()


def train_model(df: pd.DataFrame) -> XGBRegressor:
    y = df[model_configs.TIP]
    X = df.drop(columns=[model_configs.TIP])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = XGBRegressor()
    model.fit(X_train, y_train)
    return model


def main():
    df = pd.read_csv(model_path_configs.PROCESSED_DATA_PATH)
    model = train_model(df)
    model.save_model(model_path_configs.MODEL_PATH)


if __name__ == "__main__":
    main()

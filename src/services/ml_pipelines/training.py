import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

from src.database.service_manager import DatabaseServiceManager
from src.utils.configs_manager import ModelPathConfigs, ModelConfigs

model_path_configs = ModelPathConfigs.get_configs()
model_configs = ModelConfigs()
db_service_manager = DatabaseServiceManager()


def train_model(df: pd.DataFrame) -> XGBRegressor:
    y = df[model_configs.TIP]
    X = df.drop(columns=[model_configs.TIP])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = XGBRegressor()
    model.fit(X_train, y_train)
    return model


def write_trained_data_to_db(df: pd.DataFrame) -> None:
    db_service_manager.append_training_data(df)


def main():
    df = pd.read_csv(model_path_configs.PROCESSED_DATA_PATH)
    model = train_model(df)
    joblib.dump(model, model_path_configs.MODEL_PATH)
    print("Model trained and saved to disk")
    write_trained_data_to_db(df)
    print("Training data saved to database")


if __name__ == "__main__":
    main()

import pandas as pd

from src.utils.configs_manager import ModelPathConfigs
from src.utils.helper import load_yml_configs

model_path_configs = ModelPathConfigs.get_configs()


def process_data(df_input: pd.DataFrame) -> pd.DataFrame:
    df = df_input.copy()
    try:
        configs = load_yml_configs(model_path_configs.PRE_PROCESSING_CONFIGS_PATH)
        for config in configs["transformations"]:
            column = config["column"]
            if "pre_type" in config:
                df[column] = df[column].astype(config["pre_type"])
            if "mapping" in config:
                mapping = config["mapping"]
                df[column] = df[column].map(mapping)
            if "target_type" in config:
                df[column] = df[column].astype(config["target_type"])

    except Exception as e:
        raise ValueError(f"Error processing data: {str(e)}")

    return df


def main():
    df = pd.read_csv(model_path_configs.RAW_DATA_PATH)
    processed_df = process_data(df)
    processed_df.to_csv(model_path_configs.PROCESSED_DATA_PATH, index=False)


if __name__ == "__main__":
    main()

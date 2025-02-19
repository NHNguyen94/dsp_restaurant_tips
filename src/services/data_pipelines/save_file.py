import pandas as pd

from src.utils.directory_manager import DirectoryManager
from utils.configs_manager import DataPathConfigs
from utils.helper import get_unique_id

data_path_configs = DataPathConfigs()
dir_manager = DirectoryManager()


def _save_file(file_path: str, df: pd.DataFrame) -> None:
    df.to_parquet(file_path, index=False)


def _split_good_and_bad(df: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    bad_df = df[df["is_good"] == 0]
    good_df = df[df["is_good"] == 1]
    return (good_df, bad_df)


def run_save_file(df: pd.DataFrame) -> None:
    (good_df, bad_df) = _split_good_and_bad(df)
    file_name = get_unique_id()
    _save_file(data_path_configs.GOOD_DATA_PATH + "/" + file_name, good_df)
    _save_file(data_path_configs.BAD_DATA_PATH + "/" + file_name, bad_df)

import pandas as pd

from src.services.data_pipelines.models.validated_result import ValidatedResult
from src.utils.configs_manager import DataPathConfigs
from src.utils.directory_manager import DirectoryManager
from src.utils.helper import get_unique_id

data_path_configs = DataPathConfigs()
dir_manager = DirectoryManager()


def _save_file(file_path: str, df: pd.DataFrame) -> None:
    df.to_parquet(file_path, index=False)


def _split_good_and_bad(df: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    bad_df = df[df["is_good"] == 0]
    good_df = df[df["is_good"] == 1]
    return (good_df, bad_df)


def run_save_file(validated_result: ValidatedResult) -> None:
    file_name = validated_result.file_path.split("/")[-1]
    file_name = file_name + "_" + get_unique_id()
    (good_df, bad_df) = _split_good_and_bad(validated_result.final_df)
    _save_file(data_path_configs.GOOD_DATA_PATH + "/" + file_name, good_df)
    _save_file(data_path_configs.BAD_DATA_PATH + "/" + file_name, bad_df)

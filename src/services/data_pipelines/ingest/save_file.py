import pandas as pd

<<<<<<< HEAD
<<<<<<< HEAD
from src.services.data_pipelines.models.validated_result import ValidatedResult
=======
from src.services.data_pipelines.models import ValidatedResult
>>>>>>> main
=======
from src.services.data_pipelines.models import ValidatedResult
>>>>>>> main
from src.utils.configs_manager import DataPathConfigs
from src.utils.directory_manager import DirectoryManager
from src.utils.helper import get_unique_id

data_path_configs = DataPathConfigs()
dir_manager = DirectoryManager()


def _save_file(file_path: str, df: pd.DataFrame) -> None:
    df.to_csv(file_path, index=False, header=True)


def _split_good_and_bad(df: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    bad_df = df[df["is_good"] == 0]
    good_df = df[df["is_good"] == 1]
    return (good_df, bad_df)


def run_save_file(validated_result: ValidatedResult) -> None:
    file_name = validated_result.file_path.split("/")[-1]
    file_name = f"{file_name}_{get_unique_id()}.csv"
    good_df, bad_df = _split_good_and_bad(validated_result.final_df)
    if not good_df.empty:
        _save_file(f"{data_path_configs.GOOD_DATA_PATH}/{file_name}", good_df)
    if not bad_df.empty:
        _save_file(f"{data_path_configs.BAD_DATA_PATH}/{file_name}", bad_df)
    DirectoryManager.delete_file(validated_result.file_path)

import pandas as pd

from src.services.data_pipelines.models import ValidatedResult
from src.utils.configs_manager import DataPathConfigs
from src.utils.configs_manager import QualityConfigs
from src.utils.directory_manager import DirectoryManager
from src.utils.helper import get_unique_id

data_path_configs = DataPathConfigs()
dir_manager = DirectoryManager()
quality_configs = QualityConfigs()


def _save_file(file_path: str, df: pd.DataFrame) -> None:
    df.to_csv(file_path, index=False, header=True)


def _split_good_and_bad(df: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    bad_df = df[df[quality_configs.IS_GOOD] == 0]
    good_df = df[df[quality_configs.IS_GOOD] == 1]
    return (good_df, bad_df)


def run_save_file(validated_result: ValidatedResult) -> None:
    file_name = validated_result.file_path.split("/")[-1]
    file_name = f"{file_name}_{get_unique_id()}.csv"
    # Only do in case csv is parsed properly
    if validated_result.csv_results.format and validated_result.csv_results.encoding:
        if validated_result.csv_results.empty_file:
            DirectoryManager.move_file(
                validated_result.file_path,
                f"{data_path_configs.BAD_DATA_PATH}/{file_name}",
            )
        else:
            good_df, bad_df = _split_good_and_bad(validated_result.final_df)
            if not good_df.empty:
                _save_file(f"{data_path_configs.GOOD_DATA_PATH}/{file_name}", good_df)
            if not bad_df.empty:
                _save_file(f"{data_path_configs.BAD_DATA_PATH}/{file_name}", bad_df)
            DirectoryManager.delete_file(validated_result.file_path)

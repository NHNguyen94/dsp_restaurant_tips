from typing import List

import pandas as pd

from src.data_pipelines.models.bad_data import BadData, Anomaly
from src.utils.configs_manager import DataPathConfigs
from src.utils.directory_manager import DirectoryManager


class IngestionManager:
    def __init__(self):
        self.data_path_configs = DataPathConfigs.get_configs()

    def _load_files(self) -> List[str]:
        return DirectoryManager.get_file_path_in_dir(
            self.data_path_configs.RAW_DATA_PATH
        )

    def _validate_data(self, df: pd.DataFrame) -> bool:
        return True

    def _copy_good_data(self, file_path: str) -> None:
        file_name = file_path.split("/")[-1]
        DirectoryManager.move_file(
            file_path, self.data_path_configs.GOOD_DATA_PATH + "/" + file_name
        )

    def _copy_bad_data(self, file_path: str) -> None:
        file_name = file_path.split("/")[-1]
        DirectoryManager.move_file(
            file_path, self.data_path_configs.BAD_DATA_PATH + "/" + file_name
        )

    def _compute_anomaly(self, df: pd.DataFrame) -> Anomaly:
        return Anomaly(
            total_null=df.isnull().sum().sum(),
            total_missing_columns=df.isnull().any(axis=1).sum(),
            total_wrong_dtype=0,
            total_wrong_format=0,
            total_not_accept_value=0,
        )

    def _write_bad_data_to_db(self, bad_data: BadData) -> None:
        pass

    def ingest_data(self) -> None:
        files = self._load_files()
        if files:
            for file in files:
                df = pd.read_csv(file)
                if self._validate_data(df):
                    self._copy_good_data(file)
                else:
                    self._copy_bad_data(file)
                    anomaly = self._compute_anomaly(df)
                    bad_data = BadData(file_path=file, anomaly=anomaly)
                    self._write_bad_data_to_db(bad_data)

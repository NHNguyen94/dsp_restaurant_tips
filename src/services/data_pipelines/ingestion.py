import pandas as pd
from airflow import DAG

from src.utils.configs_manager import DataPathConfigs
from src.utils.directory_manager import DirectoryManager

data_path_configs = DataPathConfigs.get_configs()


def ingest_data(dag: DAG) -> None:
    with dag:
        files = DirectoryManager.get_file_path_in_dir(
            data_path_configs.RAW_DATA_PATH
        )
        if files is not None:
            for file in files:
                print(f"Reading file {file}")

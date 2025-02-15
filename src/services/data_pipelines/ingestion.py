from typing import List

import pandas as pd
from airflow import DAG

from src.data_pipelines.models.bad_data import BadData, Anomaly
from src.utils.configs_manager import DataPathConfigs
from src.utils.directory_manager import DirectoryManager

data_path_configs = DataPathConfigs.get_configs()

def _load_files() -> List[str]:
    return DirectoryManager.get_file_path_in_dir(
        data_path_configs.RAW_DATA_PATH
    )

# Only need to read into the folder and return the file paths
def ingest_data(dag: DAG) -> None:
    with dag:
        files = _load_files()
        for file in files:
            print(f"Reading file {file}")
            df = pd.read_csv(file)
            print(df.head())



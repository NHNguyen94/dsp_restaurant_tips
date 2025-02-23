import numpy as np
from airflow.exceptions import AirflowSkipException

from src.utils.configs_manager import DataPathConfigs
from src.utils.directory_manager import DirectoryManager

data_path_configs = DataPathConfigs.get_configs()


def run_ingest_data() -> str:
    files = DirectoryManager.get_file_path_in_dir(data_path_configs.RAW_DATA_PATH)
    if len(files) == 0:
        raise AirflowSkipException("No files to ingest")
    file_to_ingest = files[np.random.randint(0, len(files))]
    return file_to_ingest

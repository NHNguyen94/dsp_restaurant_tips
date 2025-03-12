import numpy as np
from airflow.exceptions import AirflowSkipException

from src.utils.configs_manager import DataPathConfigs
from src.utils.directory_manager import DirectoryManager

data_path_configs = DataPathConfigs.get_configs()


def run_ingest_data() -> str:
    files = DirectoryManager.get_file_path_in_dir(data_path_configs.RAW_DATA_PATH)
    csv_files = [file for file in files if file.endswith(".csv")]
    if len(csv_files) == 0:
        raise AirflowSkipException("No csv files to ingest")
    file_to_ingest = csv_files[np.random.randint(0, len(csv_files))]
    return file_to_ingest

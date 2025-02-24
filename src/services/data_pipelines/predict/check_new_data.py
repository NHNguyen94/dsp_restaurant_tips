from typing import List

from airflow.exceptions import AirflowSkipException

from src.database.service_manager import DatabaseServiceManager
from src.utils.configs_manager import DataPathConfigs
from src.utils.directory_manager import DirectoryManager

data_path_configs = DataPathConfigs.get_configs()
db_service_manager = DatabaseServiceManager()


def get_predicted_files(file_names: List[str]) -> List[str]:
    return db_service_manager.get_predicted_files(file_names)


def run_check_new_data() -> List[str]:
    file_names = DirectoryManager.get_file_path_in_dir(data_path_configs.GOOD_DATA_PATH)
    if len(file_names) == 0:
        raise AirflowSkipException("No new files to ingest")
    else:
        predicted_files = get_predicted_files(file_names)
        # https://www.pythonhelp.org/python-lists/how-to-subtract-two-lists-in-python/
        new_files = list(set(file_names) - set(predicted_files))
        if len(new_files) == 0:
            raise AirflowSkipException("No new files to ingest")
        return new_files

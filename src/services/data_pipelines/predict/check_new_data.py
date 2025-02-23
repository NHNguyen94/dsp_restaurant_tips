from typing import List

from airflow.exceptions import AirflowSkipException

from src.database.service_manager import DatabaseServiceManager
from src.utils.configs_manager import DataPathConfigs
from src.utils.directory_manager import DirectoryManager

data_path_configs = DataPathConfigs.get_configs()
db_service_manager = DatabaseServiceManager()


def _get_predicted_files(hours_ago: int) -> List[str]:
    predicted_files = db_service_manager.get_recent_predicted_files(hours_ago)
    if len(predicted_files) == 0:
        return []
    else:
        return [predicted_file.file_name for predicted_file in predicted_files]


def run_check_new_data(hours_ago: int) -> List[str]:
    file_names = DirectoryManager.get_file_path_in_dir(data_path_configs.RAW_DATA_PATH)
    if len(file_names) == 0:
        raise AirflowSkipException("No new files to ingest")
    else:
        predicted_file_names = _get_predicted_files(hours_ago)
        # https://www.pythonhelp.org/python-lists/how-to-subtract-two-lists-in-python/
        new_files = list(set(file_names) - set(predicted_file_names))
        if len(new_files) == 0:
            raise AirflowSkipException("No new files to ingest")
        return new_files

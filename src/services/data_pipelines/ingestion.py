import numpy as np

from src.utils.configs_manager import DataPathConfigs
from src.utils.directory_manager import DirectoryManager

data_path_configs = DataPathConfigs.get_configs()


def ingest_data() -> str:
    files = DirectoryManager.get_file_path_in_dir(data_path_configs.RAW_DATA_PATH)
    return files[np.random.randint(0, len(files))]

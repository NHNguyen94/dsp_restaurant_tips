import os
import sys

import numpy as np
import pandas as pd

from src.utils.configs_manager import DataPathConfigs
from src.utils.helper import get_unique_id

data_path_configs = DataPathConfigs.get_configs()


def split_data(file_path: str, folder_path: str, number_of_files: int):
    data = pd.read_csv(file_path)
    file_name = file_path.split("/")[-1]
    data_split = np.array_split(data, number_of_files)
    for i in range(number_of_files):
        data_split[i].to_csv(
            os.path.join(folder_path, f"{file_name}_" + get_unique_id() + ".csv"),
            index=False,
        )


if __name__ == "__main__":
    split_data(
        f"{data_path_configs.DATASET_PATH}",
        f"{data_path_configs.RAW_DATA_PATH}",
        int(sys.argv[1]),
    )

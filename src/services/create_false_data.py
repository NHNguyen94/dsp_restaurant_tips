import numpy as np
import pandas as pd

from src.utils.configs_manager import DataPathConfigs
from src.utils.helper import get_unique_id

data_path_configs = DataPathConfigs.get_configs()


def _create_correct_data(n: int) -> pd.DataFrame:
    total_bill_list = []
    sex_list = []
    smoker_list = []
    day_list = []
    time_list = []
    size_list = []
    for i in range(n):
        total_bill_list.append(np.random.uniform(0, 1000))
        sex_list.append(np.random.choice(["Male", "Female"]))
        smoker_list.append(np.random.choice(["Yes", "No"]))
        day_list.append(
            np.random.choice(["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"])
        )
        time_list.append(np.random.choice(["Lunch", "Dinner"]))
        size_list.append(np.random.randint(1, 10))
    data = {
        "total_bill": total_bill_list,
        "sex": sex_list,
        "smoker": smoker_list,
        "day": day_list,
        "time": time_list,
        "size": size_list,
    }
    return pd.DataFrame(data)


def _create_false_data(n: int) -> pd.DataFrame:
    total_bill_list = []
    sex_list = []
    smoker_list = []
    day_list = []
    time_list = []
    size_list = []
    for i in range(n):
        total_bill_list.append(np.random.choice(["a", "b", None]))
        sex_list.append(np.random.choice(["Non-Binary", "Unknown", None]))
        smoker_list.append(np.random.choice(["Maybe", "Maybe Not", None]))
        day_list.append(np.random.choice(["Weekday", "Weekend", None]))
        time_list.append(np.random.choice(["Breakfast", "Supper", None]))
        size_list.append(np.random.choice([-1, -2, None]))
    data = {
        "total_bill": total_bill_list,
        "sex": sex_list,
        "smoker": smoker_list,
        "day": day_list,
        "time": time_list,
        "size": size_list,
    }
    return pd.DataFrame(data)


def create_false_and_correct_data(n: int) -> pd.DataFrame:
    correct_data = _create_correct_data(n)
    false_data = _create_false_data(n)
    return pd.concat([correct_data, false_data], ignore_index=True)


def create_df_missing_column(n: int) -> pd.DataFrame:
    df = _create_correct_data(n)
    df_missing_col = df.drop(columns=["size"])
    return df_missing_col


def create_csv_with_custom_delimiter(n: int, delimiter: str, file_path: str) -> None:
    df = _create_correct_data(n)
    df.to_csv(file_path, sep=delimiter, index=False)


def create_empty_csv(file_path: str) -> None:
    df = pd.DataFrame()
    df.to_csv(file_path, index=False)


def create_empty_csv_with_header(file_path: str) -> None:
    df = pd.DataFrame(
        columns=["total_bill", "tip", "sex", "smoker", "day", "time", "size"]
    )
    df.to_csv(file_path, index=False)


def main(n: int):
    df_false_data = create_false_and_correct_data(n)
    df_false_data.to_csv(
        f"{data_path_configs.RAW_DATA_PATH}/false_data_{get_unique_id()}.csv",
        index=False,
    )
    df_missing_col = create_df_missing_column(n)
    df_missing_col.to_csv(
        f"{data_path_configs.RAW_DATA_PATH}/missing_columns_{get_unique_id()}.csv",
        index=False,
    )
    create_csv_with_custom_delimiter(
        n,
        "\t",
        f"{data_path_configs.RAW_DATA_PATH}/custom_delimiter_{get_unique_id()}.csv",
    )
    create_empty_csv(
        f"{data_path_configs.RAW_DATA_PATH}/empty_csv_{get_unique_id()}.csv"
    )
    create_empty_csv_with_header(
        f"{data_path_configs.RAW_DATA_PATH}/empty_csv_with_header_{get_unique_id()}.csv"
    )


if __name__ == "__main__":
    main(int(20))

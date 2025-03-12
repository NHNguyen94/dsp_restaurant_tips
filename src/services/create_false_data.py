import numpy as np
import pandas as pd

from src.utils.configs_manager import DataPathConfigs
from src.utils.helper import get_unique_id

data_path_configs = DataPathConfigs.get_configs()


def _get_random_total_bill() -> float:
    return np.random.uniform(0, 1000)


def _get_random_sex() -> str:
    return np.random.choice(["Male", "Female"])


def _get_random_smoker() -> str:
    return np.random.choice(["Yes", "No"])


def _get_random_day() -> str:
    return np.random.choice(["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"])


def _get_random_time() -> str:
    return np.random.choice(["Lunch", "Dinner"])


def _get_random_size() -> int:
    return np.random.randint(1, 10)


def _create_correct_data(n: int) -> pd.DataFrame:
    total_bill_list = []
    sex_list = []
    smoker_list = []
    day_list = []
    time_list = []
    size_list = []
    for i in range(n):
        total_bill_list.append(_get_random_total_bill())
        sex_list.append(_get_random_sex())
        smoker_list.append(_get_random_smoker())
        day_list.append(_get_random_day())
        time_list.append(_get_random_time())
        size_list.append(_get_random_size())
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
        size_list.append(np.random.choice(["one", "two", None]))
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
    df = create_false_and_correct_data(n)
    df.to_csv(file_path, sep=delimiter, index=False)


def main(n: int):
    df_false_data = create_false_and_correct_data(n)
    df_false_data.to_csv(
        f"{data_path_configs.RAW_DATA_PATH}/{get_unique_id()}_false_data.csv",
        index=False,
    )
    df_missing_col = create_df_missing_column(n)
    df_missing_col.to_csv(
        f"{data_path_configs.RAW_DATA_PATH}/{get_unique_id()}_missing_columns.csv",
        index=False,
    )
    create_csv_with_custom_delimiter(
        n,
        "\t",
        f"{data_path_configs.RAW_DATA_PATH}/{get_unique_id()}_custom_delimiter.csv",
    )


if __name__ == "__main__":
    main(int(10))

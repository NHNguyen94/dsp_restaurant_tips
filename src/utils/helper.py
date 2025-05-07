import subprocess
import uuid
from typing import Dict, List

import numpy as np
import pandas as pd
import yaml


def load_yml_configs(config_path: str) -> Dict:
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def round_number(number: float, decimal_places: int = 2) -> float:
    return float(str(round(number, decimal_places)))


def get_current_user() -> str:
    return subprocess.check_output("whoami", encoding="utf-8").strip()


def get_unique_id() -> str:
    return str(uuid.uuid4())


def is_number(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def remove_numerical_values(list_values: List) -> List:
    new_list = [x for x in list_values if not is_number(x)]
    return [str(x) for x in new_list] if new_list else []


def remove_non_numerical_values(list_values: List) -> List:
    new_list = [x for x in list_values if is_number(x)]
    return [float(x) for x in new_list] if new_list else []


def find_non_numerical_values_in_df(df: pd.DataFrame, col: str) -> List[str]:
    new_df = df.copy()
    new_df = new_df.dropna(subset=[col])
    return new_df[~new_df[col].apply(lambda x: is_number(x))][col].tolist()


def find_numerical_values_in_df(df: pd.DataFrame, col: str) -> List[str]:
    new_df = df.copy()
    new_df = new_df.dropna(subset=[col])
    return new_df[new_df[col].apply(lambda x: is_number(x))][col].tolist()


def generate_random_number(start: int, end: int) -> float:
    return np.random.uniform(start, end)

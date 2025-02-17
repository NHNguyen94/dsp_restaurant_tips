import subprocess
from typing import Dict

import yaml


def load_configs(config_path) -> Dict:
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def round_number(number: float, decimal_places: int = 2) -> float:
    return float(str(round(number, decimal_places)))


def get_current_user() -> str:
    return subprocess.check_output("whoami", encoding="utf-8").strip()

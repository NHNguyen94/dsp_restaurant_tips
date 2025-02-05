from typing import Dict

import yaml


def load_configs(config_path) -> Dict:
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

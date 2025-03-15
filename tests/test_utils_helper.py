import pandas as pd

from src.utils.configs_manager import ModelPathConfigs
from src.utils.date_time_manager import DateTimeManager
from src.utils.helper import (
    load_yml_configs,
    round_number,
    get_unique_id,
    find_non_numerical_values_in_df,
    find_numerical_values_in_df,
)


class TestUtilsHelper:
    date_time_manager = DateTimeManager()

    def test_load_configs(self):
        configs = load_yml_configs(ModelPathConfigs.PRE_PROCESSING_CONFIGS_PATH)
        assert configs is not None
        assert configs["transformations"] is not None

    def test_round_number(self):
        number = 10.123456
        rounded_number = round_number(number)
        assert rounded_number == 10.12

    def test_get_unique_id(self):
        unique_id = get_unique_id()
        assert unique_id is not None
        assert len(unique_id) > 0

    def test_parse_str_to_date(self):
        date = "2021-01-01"
        parsed_date = self.date_time_manager.parse_str_to_date(date)
        assert parsed_date.year == 2021
        assert parsed_date.month == 1
        assert parsed_date.day == 1
        assert str(parsed_date) == "2021-01-01"

    def test_find_non_numerical_values_in_df(self):
        df = pd.DataFrame({"col": ["1", "2.2", "3.3.3", "a", "b", "c", None]})
        non_numerical_values = find_non_numerical_values_in_df(df, "col")
        assert non_numerical_values == ["3.3.3", "a", "b", "c"]

    def test_find_numerical_values_in_df(self):
        df = pd.DataFrame({"col": ["1", "2.2", "3.3.3", "a", "b", "c", None]})
        numerical_values = find_numerical_values_in_df(df, "col")
        assert numerical_values == ["1", "2.2"]

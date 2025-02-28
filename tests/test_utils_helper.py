from src.utils.configs_manager import ModelPathConfigs
from src.utils.helper import load_configs, round_number, get_unique_id
from src.utils.date_time_manager import DateTimeManager


class TestUtilsHelper:
    date_time_manager = DateTimeManager()

    def test_load_configs(self):
        configs = load_configs(ModelPathConfigs.PRE_PROCESSING_CONFIGS_PATH)
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

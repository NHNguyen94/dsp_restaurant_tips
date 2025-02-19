from src.utils.configs_manager import ModelPathConfigs
from src.utils.helper import load_configs, round_number, get_unique_id


class TestUtilsHelper:
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

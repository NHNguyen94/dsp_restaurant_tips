from src.utils.configs_manager import ModelPathConfigs
from src.utils.helper import load_configs


class TestUtilsHelper:

    def test_load_configs(self):
        configs = load_configs(ModelPathConfigs.PRE_PROCESSING_CONFIGS_PATH)
        assert configs is not None
        assert configs["transformations"] is not None

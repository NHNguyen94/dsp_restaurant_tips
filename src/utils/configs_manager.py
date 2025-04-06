from abc import ABC, abstractmethod

from src.utils.directory_manager import DirectoryManager


class PathConfigs(ABC):
    @staticmethod
    @abstractmethod
    def create_needed_directories():
        pass

    @staticmethod
    @abstractmethod
    def get_configs():
        pass


class DataPathConfigs(PathConfigs):
    DATASET_PATH = "src/data/tips.csv"
    RAW_DATA_PATH = "src/data/raw_data"
    GOOD_DATA_PATH = "src/data/good_data"
    BAD_DATA_PATH = "src/data/bad_data"

    @staticmethod
    def create_needed_directories():
        DirectoryManager.create_dir_if_not_exists("src/data/raw_data")
        DirectoryManager.create_dir_if_not_exists("src/data/good_data")
        DirectoryManager.create_dir_if_not_exists("src/data/bad_data")

    @staticmethod
    def get_configs():
        DataPathConfigs.create_needed_directories()
        return DataPathConfigs


class ModelPathConfigs(PathConfigs):
    MODEL_PATH = "src/data_ml_models/models/tips_model.joblib"
    PRE_PROCESSING_CONFIGS_PATH = "src/configs/pre_processing_configs.yml"
    RAW_DATA_PATH = DataPathConfigs.DATASET_PATH
    PROCESSED_DATA_PATH = "src/data_ml_models/processed/tips.parquet"
    TEST_DATA_PATH = "src/data_ml_models/test/tips.csv"

    @staticmethod
    def create_needed_directories():
        DirectoryManager.create_dir_if_not_exists("src/data_ml_models/models")
        DirectoryManager.create_dir_if_not_exists("src/data_ml_models/processed")

    @staticmethod
    def get_configs():
        ModelPathConfigs.create_needed_directories()
        return ModelPathConfigs


class ModelConfigs:
    TIP = "tip"


class DataConfigs:
    DEFAULT_DECODER = "utf-8"
    DEFAULT_DELIMITER = ","
    ACCEPTED_ENCODINGS = ["utf-8", "ascii"]
    EXPECTED_RESULTS_FOR_VALIDATION = {
        "total_bill": {"min": 0, "max": 1000000, "type": "float"},
        "size": {"min": 0, "max": 50, "type": "int"},
        "sex": {"accept": ("Male", "Female"), "type": "str"},
        "smoker": {"accept": ("Yes", "No"), "type": "str"},
        "day": {
            "accept": ("Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"),
            "type": "str",
        },
        "time": {"accept": ("Lunch", "Dinner"), "type": "str"},
    }


class QualityConfigs:
    IS_GOOD = "is_good"
    COLUMN_NOT_EXIST = "column_not_exist"
    NULL_VALUE = "null_value"
    WRONG_DATA_TYPE = "wrong_data_type"
    OUT_OF_RANGE = "out_of_range"

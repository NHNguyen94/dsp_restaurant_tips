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
    MODEL_PATH = "src/data_ml_models/models/tips_model.json"
    PRE_PROCESSING_CONFIGS_PATH = "src/configs/pre_processing_configs.yml"
    RAW_DATA_PATH = "src/data_ml_models/raw/tips.csv"
    PROCESSED_DATA_PATH = "src/data_ml_models/processed/tips.parquet"
    TEST_DATA_PATH = "src/data_ml_models/test/tips.csv"

    @staticmethod
    def create_needed_directories():
        DirectoryManager.create_dir_if_not_exists("src/data_ml_models/models")
        DirectoryManager.create_dir_if_not_exists("src/data_ml_models/raw")
        DirectoryManager.create_dir_if_not_exists("src/data_ml_models/processed")

    @staticmethod
    def get_configs():
        ModelPathConfigs.create_needed_directories()
        return ModelPathConfigs

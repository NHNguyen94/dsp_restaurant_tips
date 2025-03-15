import os

from src.services.split_data import split_data
from src.utils.directory_manager import DirectoryManager


class TestSplitData:
    def test_split_data(self):
        raw_data_path = "src/data/tips.csv"
        folder_path = "tests/resources/generated_data"
        DirectoryManager.create_dir_if_not_exists(folder_path)
        number_of_files = 25
        curr_file_count = len(
            [
                f
                for f in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, f))
            ]
        )
        split_data(raw_data_path, folder_path, number_of_files)
        real_file_count = (
            len(
                [
                    f
                    for f in os.listdir(folder_path)
                    if os.path.isfile(os.path.join(folder_path, f))
                ]
            )
            - curr_file_count
        )
        generated_files = DirectoryManager.get_file_path_in_dir(folder_path)
        assert real_file_count == number_of_files
        assert len(generated_files) == number_of_files
        for file in generated_files:
            DirectoryManager.delete_file(file)

from src.utils import DirectoryManager


class TestDirectoryManager:
    non_exist_test_file_path = "tests/resources/test_folder_1/test_file_2.txt"
    exist_test_file_path = "tests/resources/test_folder_1/test_file_1.txt"
    non_exist_test_folder_path = "tests/resources/test_folder_2"
    exist_test_folder_path = "tests/resources/test_folder_1"

    def test_check_if_dir_exists(self):
        assert DirectoryManager.check_if_dir_exists(self.exist_test_folder_path) == True
        assert (
            DirectoryManager.check_if_dir_exists(self.non_exist_test_folder_path)
            == False
        )

    def test_create_dir_if_not_exists(self):
        DirectoryManager.create_dir_if_not_exists(self.non_exist_test_folder_path)
        assert (
            DirectoryManager.check_if_dir_exists(self.non_exist_test_folder_path)
            == True
        )
        DirectoryManager.delete_empty_dir(self.non_exist_test_folder_path)
        assert (
            DirectoryManager.check_if_dir_exists(self.non_exist_test_folder_path)
            == False
        )

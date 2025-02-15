def _copy_good_data(self, file_path: str) -> None:
    file_name = file_path.split("/")[-1]
    DirectoryManager.move_file(
        file_path, self.data_path_configs.GOOD_DATA_PATH + "/" + file_name
    )


def _copy_bad_data(self, file_path: str) -> None:
    file_name = file_path.split("/")[-1]
    DirectoryManager.move_file(
        file_path, self.data_path_configs.BAD_DATA_PATH + "/" + file_name
    )
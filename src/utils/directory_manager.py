import os
from typing import List, Union


class DirectoryManager:
    @staticmethod
    def print_current_dir() -> None:
        print(os.getcwd())

    @staticmethod
    def check_if_dir_exists(dir: str) -> bool:
        return os.path.exists(dir)

    @staticmethod
    def create_dir_if_not_exists(dir: str) -> None:
        if not DirectoryManager.check_if_dir_exists(dir):
            os.makedirs(dir)
            print(f"Directory {dir} created")
        else:
            print(f"Directory {dir} already exists")

    @staticmethod
    def check_if_file_exists(file_path: str) -> bool:
        return os.path.exists(file_path)

    @staticmethod
    def move_file(src: str, dest: str) -> None:
        os.rename(src, dest)
        print(f"File {src} moved to {dest}")

    @staticmethod
    def delete_file(file_path: str) -> None:
        os.remove(file_path)
        print(f"File {file_path} deleted")

    @staticmethod
    def delete_empty_dir(dir: str) -> None:
        os.rmdir(dir)
        print(f"Directory {dir} deleted")

    @staticmethod
    def get_file_path_in_dir(folder_path: str) -> Union[List[str], None]:
        if DirectoryManager.check_if_dir_exists(folder_path):
            return [
                os.path.join(folder_path, file)
                for file in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, file))
            ]
        else:
            return None

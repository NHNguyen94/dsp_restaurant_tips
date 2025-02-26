# from services.data_pipelines.ingest.split_data import split_data
# from src.utils.directory_manager import DirectoryManager
# import os
#
#
# class TestSplitData:
#     def test_split_data(self):
#         rawDataPath = "src/data/raw_data/dataset.csv"
#         folderPath = "tests/resources/generated_data"
#         numberOfFiles = 25
#         curr_file_count = len(
#             [
#                 f
#                 for f in os.listdir(folderPath)
#                 if os.path.isfile(os.path.join(folderPath, f))
#             ]
#         )
#         split_data(rawDataPath, folderPath, numberOfFiles)
#         real_file_count = (
#             len(
#                 [
#                     f
#                     for f in os.listdir(folderPath)
#                     if os.path.isfile(os.path.join(folderPath, f))
#                 ]
#             )
#             - curr_file_count
#         )
#         assert real_file_count == numberOfFiles
#         generated_files = DirectoryManager.get_file_path_in_dir(
#             "tests/resources/generated_data"
#         )
#         for i in range(len(generated_files)):
#             if ".gitkeep" not in generated_files[i]:
#                 DirectoryManager.delete_file(generated_files[i])

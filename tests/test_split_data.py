from src.services.data_pipelines.split_data import split_data
import os

class TestSplitData:
    def test_split_data(self):
        rawDataPath = 'src/data/raw_data/dataset.csv'
        folderPath = 'src/data/generated_data'
        numberOfFiles = 25
        curr_file_count = len([f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, f))])
        split_data(rawDataPath, folderPath, numberOfFiles)
        real_file_count = len([f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, f))]) - curr_file_count
        assert real_file_count == numberOfFiles
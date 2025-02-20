import pandas as pd
import numpy as np
import os
import sys
# Get the absolute path of the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
# Add the project root to the Python path
sys.path.append(project_root)
# Import the function
from src.utils.helper import get_unique_id


def split_data(filePath, folderPath, nbrOfFiles):
    # Load data
    data = pd.read_csv(filePath)

    # Split data
    data_split = np.array_split(data, nbrOfFiles)

    # Save data
    for i in range(nbrOfFiles):
        data_split[i].to_csv(os.path.join(folderPath, 'data_' + get_unique_id() + '.csv'), index=False)


split_data('src/data/raw_data/dataset.csv', 'src/data/generated_data', 25)

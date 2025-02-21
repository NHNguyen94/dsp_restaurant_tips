import pandas as pd
import numpy as np
import os
import sys
from src.utils.helper import get_unique_id

def split_data(filePath, folderPath, nbrOfFiles):
    # Load data
    data = pd.read_csv(filePath)

    # Split data
    data_split = np.array_split(data, nbrOfFiles)

    # Save data
    for i in range(nbrOfFiles):
        data_split[i].to_csv(os.path.join(folderPath, 'data_' + get_unique_id() + '.csv'), index=False)

#Only do that if file is executed, not when its imported
if __name__ == "__main__":
    split_data('src/data/raw_data/dataset.csv', 'src/data/generated_data', int(sys.argv[1]))

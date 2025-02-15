import pandas as pd

from src.services.ml_pipelines import process_data


class TestProcessData:
    def test_process_data(self):
        df = pd.DataFrame(
            {
                "tip": [1, 2, 3],
                "total_bill": [16.99, 10.34, 21.01],
                "sex": ["Male", "Female", "Male"],
                "smoker": [False, False, True],
                "day": ["Sun", "Thur", "Sat"],
                "time": ["Dinner", "Lunch", "Dinner"],
                "size": [2, 3, 5],
            }
        )
        processed_df = process_data(df)
        assert processed_df.shape == df.shape
        assert processed_df["sex"].dtype == "int64"
        assert processed_df["smoker"].dtype == "int64"
        assert processed_df["day"].dtype == "int64"
        assert processed_df["time"].dtype == "int64"

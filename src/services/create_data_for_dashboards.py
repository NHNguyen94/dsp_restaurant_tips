import numpy as np
import pandas as pd

from src.database.service_manager import DatabaseServiceManager
from src.utils.date_time_manager import DateTimeManager

db_service_manager = DatabaseServiceManager()


def create_data_issues(n: int, from_days_ago: int) -> pd.DataFrame:
    evaluated_expectations_list = []
    successful_expectations_list = []
    unsuccessful_expectations_list = []
    success_percent_list = []
    missing_columns_list = []
    missing_values_list = []
    duplicated_rows_list = []
    unknown_categorical_values_list = []
    unknon_numeric_values_list = []
    bad_csv_encoding_list = []
    bad_csv_format_list = []
    other_parse_issues_list = []
    total_rows_list = []
    total_bad_rows_list = []
    created_at_list = []
    for i in range(n):
        evaluated_expectations_list.append(np.random.randint(0, 20))
        successful_expectations_list.append(np.random.randint(0, 20))
        unsuccessful_expectations_list.append(np.random.randint(0, 20))
        success_percent_list.append(np.random.uniform(0, 100))
        missing_columns_list.append(np.random.randint(0, 2))
        missing_values_list.append(np.random.randint(0, 20))
        duplicated_rows_list.append(np.random.randint(0, 20))
        unknown_categorical_values_list.append(np.random.randint(0, 20))
        unknon_numeric_values_list.append(np.random.randint(0, 20))
        bad_csv_encoding_list.append(np.random.randint(0, 20))
        bad_csv_format_list.append(np.random.randint(0, 1))
        other_parse_issues_list.append(np.random.randint(0, 1))
        total_rows_list.append(np.random.randint(0, 1))
        total_bad_rows_list.append(np.random.randint(0, 1))
        created_at_list.append(DateTimeManager.get_random_time_before_now(from_days_ago))
    data = {
        "evaluated_expectations": evaluated_expectations_list,
        "successful_expectations": successful_expectations_list,
        "unsuccessful_expectations": unsuccessful_expectations_list,
        "success_percent": success_percent_list,
        "missing_columns": missing_columns_list,
        "missing_values": missing_values_list,
        "duplicated_rows": duplicated_rows_list,
        "unknown_categorical_values": unknown_categorical_values_list,
        "unknon_numeric_values": unknon_numeric_values_list,
        "bad_csv_encoding": bad_csv_encoding_list,
        "bad_csv_format": bad_csv_format_list,
        "other_parse_issues": other_parse_issues_list,
        "total_rows": total_rows_list,
        "total_bad_rows": total_bad_rows_list,
        "created_at": created_at_list
    }
    return pd.DataFrame(data)


def create_predictions(n: int, from_days_ago: int) -> pd.DataFrame:
    total_bill_list = []
    sex_list = []
    smoker_list = []
    day_list = []
    time_list = []
    size_list = []
    tip_list = []
    predicted_at_list = []
    for i in range(n):
        total_bill_list.append(np.random.uniform(0, 1000))
        sex_list.append(np.random.choice(["Male", "Female"]))
        smoker_list.append(np.random.choice(["Yes", "No"]))
        day_list.append(
            np.random.choice(["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"])
        )
        time_list.append(np.random.choice(["Lunch", "Dinner"]))
        size_list.append(np.random.randint(1, 10))
        tip_list.append(np.random.uniform(0, 100))
        predicted_at_list.append(DateTimeManager.get_random_time_before_now(from_days_ago))
    data = {
        "total_bill": total_bill_list,
        "sex": sex_list,
        "smoker": smoker_list,
        "day": day_list,
        "time": time_list,
        "size": size_list,
        "tip": tip_list,
        "predicted_at": predicted_at_list,
    }
    return pd.DataFrame(data)


def main(n: int, from_days_ago: int):
    df_predictions = create_predictions(n, from_days_ago)
    db_service_manager.append_df_to_predictions_with_existing_predicted_at(
        df_predictions,
        "auto_gen_for_dashboards",
        "scheduled_predictions"
    )
    df_data_issues = create_data_issues(n, from_days_ago)
    db_service_manager.append_df_to_data_issues_with_existing_created_at(
        df_data_issues,
        "auto_gen_for_dashboards"
    )


if __name__ == "__main__":
    n = 500
    from_days_ago = 7
    main(n, from_days_ago)

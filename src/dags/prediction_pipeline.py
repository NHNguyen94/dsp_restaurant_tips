import datetime
import os
import sys
from typing import List

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_dir)
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from src.services.data_pipelines.predict import run_predictions, check_new_data


@dag(
    dag_id="prediction_pipeline",
    description="Prediction pipeline",
    tags=["prediction"],
    schedule_interval=datetime.timedelta(seconds=60),
    start_date=days_ago(1, hour=23, minute=55),
    max_active_runs=1,
    catchup=False,
)
def prediction_pipeline():
    @task
    def check_for_new_data() -> List[str]:
        return check_new_data.run_check_new_data()

    @task
    def make_predictions(new_files: List[str]) -> None:
        run_predictions(new_files, "scheduled_predictions")

    new_files = check_for_new_data()
    make_predictions(new_files)


prediction_pipeline()

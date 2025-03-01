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
    start_date=days_ago(n=0, hour=1),
    max_active_runs=1,
    catchup=False,
)
def prediction_pipeline():
    @task
    def build_check_new_data() -> List[str]:
        return check_new_data.run_check_new_data()

    @task
    def build_predictions(new_files: List[str]) -> None:
<<<<<<< HEAD
        run_predictions(new_files)
=======
        run_predictions(new_files, "scheduled_predictions")
>>>>>>> main

    new_files = build_check_new_data()
    build_predictions(new_files)


prediction_pipeline()

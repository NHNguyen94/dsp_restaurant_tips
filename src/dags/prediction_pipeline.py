import datetime
import os
import sys
from typing import List

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_dir)

from airflow.decorators import dag, task
from src.services.data_pipelines.predict import run_check_new_data, run_prediction
from airflow.utils.dates import days_ago
import asyncio


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
    def check_for_new_data() -> List[str]:
        return run_check_new_data(hours_ago=1)

    @task
    def make_prediction(file_paths: List[str]) -> None:
        asyncio.run(run_prediction(file_paths))

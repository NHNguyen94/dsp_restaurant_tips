import datetime
import os
import sys

import pandas as pd
from airflow.decorators import dag, task

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_dir)

from src.services.data_pipelines import (
    run_ingest_data,
    run_validate_data,
    run_save_file,
)

from airflow.utils.dates import days_ago


@dag(
    dag_id="ingestion_pipeline",
    description="Ingestion pipeline",
    tags=["ingestion"],
    schedule_interval=datetime.timedelta(seconds=60),
    start_date=days_ago(n=0, hour=1),
    max_active_runs=1,
    catchup=False,
)
def ingestion_pipeline():
    @task
    def ingest() -> str:
        return run_ingest_data()

    @task
    def build_validate(file_path: str) -> pd.DataFrame:
        return run_validate_data(file_path)

    @task
    def build_alert(df: pd.DataFrame) -> None:
        pass

    @task
    def build_save_file(df: pd.DataFrame) -> None:
        run_save_file(df)

    @task
    def build_save_statistics(bad_data: pd.DataFrame) -> None:
        pass

    ingested_file = ingest()
    df = build_validate(file_path=ingested_file)
    build_alert(df)
    build_save_file(df)
    build_save_statistics(df)


ingestion_pipeline()

import datetime
import os
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_dir)

from airflow.decorators import dag, task

from services.data_pipelines.models import ValidatedResult

from src.services.data_pipelines.ingest import (
    run_ingest_data,
    run_validate_data,
    run_save_file,
    run_alert,
    run_save_statistics,
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
    def build_validate(file_path: str) -> ValidatedResult:
        return run_validate_data(file_path, "batch for ingestion pipeline")

    @task
    def build_alert(validated_result: ValidatedResult) -> None:
        run_alert(validated_result)

    @task
    def build_save_file(validated_result: ValidatedResult) -> None:
        run_save_file(validated_result)

    @task
    def build_save_statistics(validated_result: ValidatedResult) -> None:
        run_save_statistics(validated_result)

    ingested_file = ingest()
    validated_result = build_validate(ingested_file)
    build_alert(validated_result)
    build_save_file(validated_result)
    build_save_statistics(validated_result)


ingestion_pipeline()

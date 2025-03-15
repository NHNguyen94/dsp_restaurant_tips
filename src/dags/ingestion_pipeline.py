import datetime
import logging
import os
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_dir)

from airflow.decorators import dag, task
from airflow.exceptions import AirflowSkipException
from src.services.data_pipelines.models import ValidatedResult
from src.services.data_pipelines.ingest import (
    run_ingest_data,
    run_validate_data,
    run_save_file,
    run_alert,
    run_save_statistics,
)
from airflow.utils.dates import days_ago
from src.utils.csv_parser import CSVParser

csv_parser = CSVParser()


@dag(
    dag_id="ingestion_pipeline",
    description="Ingestion pipeline",
    tags=["ingestion"],
    schedule_interval=datetime.timedelta(seconds=60),
    start_date=days_ago(1, hour=23, minute=55),
    max_active_runs=1,
    catchup=False,
)
def ingestion_pipeline():
    @task
    def ingest() -> str:
        return run_ingest_data()

    @task
    def build_validate(file_path: str) -> ValidatedResult:
<<<<<<< HEAD
=======
        df = csv_parser.read_csv_from_file_path(file_path)
        if len(df) == 0:
            raise AirflowSkipException("Empty dataframe")
>>>>>>> main
        validated_result = run_validate_data(file_path, "batch for ingestion pipeline")
        logging.debug(f"validated_result: {validated_result}")
        return validated_result

    @task
    def build_alert(validated_result: ValidatedResult) -> None:
        if validated_result.overall_result == False:
            run_alert(validated_result)

    @task
    def build_save_file(validated_result: ValidatedResult) -> None:
        run_save_file(validated_result)

    @task
    def build_save_statistics(validated_result: ValidatedResult) -> None:
        if validated_result.overall_result == False:
            run_save_statistics(validated_result)

    ingested_file = ingest()
    validated_result = build_validate(ingested_file)
    build_alert(validated_result)
    build_save_file(validated_result)
    build_save_statistics(validated_result)


ingestion_pipeline()

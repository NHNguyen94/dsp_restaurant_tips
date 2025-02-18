import datetime

import os
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_dir)
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from src.services.data_pipelines import ingest_data


def build_ingest(dag: DAG):
    return PythonOperator(
        task_id="ingest_data",
        python_callable=ingest_data,
        dag=dag,
    )


def build_validate(dag: DAG):
    return EmptyOperator(task_id="validate_data", dag=dag)


def build_alert(dag: DAG):
    return EmptyOperator(task_id="send_alert", dag=dag)


def build_save_file(dag: DAG):
    return EmptyOperator(task_id="save_file", dag=dag)


def build_save_statistics(dag: DAG):
    return EmptyOperator(task_id="save_statistics", dag=dag)


def build_clear_cache(dag: DAG):
    return EmptyOperator(task_id="clear_cache", dag=dag)


def build_prod_dag(dag: DAG):
    ingest = build_ingest(dag)
    validate = build_validate(dag)
    alert = build_alert(dag)
    save_file = build_save_file(dag)
    stats = build_save_statistics(dag)
    clear_cache = build_clear_cache(dag)

    ingest >> validate
    validate >> alert
    validate >> save_file
    validate >> stats
    alert >> clear_cache
    save_file >> clear_cache
    stats >> clear_cache


my_dag = DAG(
    dag_id="ingestion_pipeline",
    start_date=datetime.datetime(2025, 2, 14),
    # https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/cron.html
    schedule=datetime.timedelta(seconds=60),
)

build_prod_dag(my_dag)

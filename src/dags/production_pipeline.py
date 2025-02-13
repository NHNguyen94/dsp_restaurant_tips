import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator


def build_ingest(dag: DAG):
    return EmptyOperator(task_id="read_data", dag=dag)


def build_validate(dag: DAG):
    return EmptyOperator(task_id="validate_data", dag=dag)


def build_alert(dag: DAG):
    return EmptyOperator(task_id="send_alert", dag=dag)


def build_save_file(dag: DAG):
    return EmptyOperator(task_id="save_file", dag=dag)


def save_statistics(dag: DAG):
    return EmptyOperator(task_id="save_statistics", dag=dag)


def build_prod_dag(dag: DAG):
    ingest = build_ingest(dag)
    validate = build_validate(dag)
    alert = build_alert(dag)
    save_file = build_save_file(dag)
    stats = save_statistics(dag)

    ingest >> validate
    validate >> alert
    validate >> save_file
    validate >> stats


my_dag = DAG(
    dag_id="production_pipeline",
    start_date=datetime.datetime(2025, 2, 14),
    # https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/cron.html
    schedule=datetime.timedelta(seconds=60)
)

build_prod_dag(my_dag)

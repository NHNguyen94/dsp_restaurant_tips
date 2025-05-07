import logging
import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

DB_CREDENTIALS = {
    "dbname": "postgres_db",
    "user": "admin_user",
    "password": "admin_password",
    "host": "localhost",
    "port": 5432,
}


def test_db_read():
    try:
        conn = psycopg2.connect(**DB_CREDENTIALS)
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        logging.info(f"Query Result: {result}")
        assert result == (1,), "Database query failed!"
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise


default_args = {"owner": "airflow", "start_date": datetime(2024, 1, 1)}
dag = DAG("test_db_dag", default_args=default_args, schedule_interval=None)

test_db_task = PythonOperator(
    task_id="test_db_connection", python_callable=test_db_read, dag=dag
)


def test_dag():
    print(f"\n\nDAG: {dag.dag_id} is ready to be used.\n\n")
    print(f"\ntest_db_task: {test_db_task.task_id} is ready to be used.\n\n")

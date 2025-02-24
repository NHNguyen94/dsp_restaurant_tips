import datetime
import logging
import os
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_dir)
import psycopg2
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago


@dag(
    dag_id="prediction_pipeline",
    description="Prediction pipeline",
    tags=["prediction"],
    schedule_interval=datetime.timedelta(seconds=60),
    start_date=days_ago(n=0, hour=1),
    max_active_runs=1,
    catchup=False,
)
def run_connect_db():
    @task
    def connect_to_another_db():
        try:
            db_params = {
                "host": "localhost",
                "database": "postgres_db",
                "user": "admin_user",
                "password": "admin_password",
            }
            conn = psycopg2.connect(**db_params)
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
            if result:
                logging.warning("Successfully connected to the database!")
                logging.warning(f"Query result: {result}")
            else:
                logging.warning("No result from the query.")
            cursor.close()
            conn.close()

        except Exception as e:
            logging.warning(f"Error during connection setup or query execution: {e}")

    connect_to_another_db()


run_connect_db()

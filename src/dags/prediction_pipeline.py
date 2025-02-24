import datetime
import logging
import os
import sys

from airflow.hooks.base import BaseHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.session import provide_session

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_dir)

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
    # set timeout
    default_args={"execution_timeout": datetime.timedelta(minutes=5)},
    dagrun_timeout=datetime.timedelta(minutes=5),
)
def prediction_pipeline():
    @task
    def run_connect_to_db():
        # connect_to_db()
        fetch_conn()

    @provide_session
    def fetch_conn(session=None):
        import sys
        logging.warning(f"Airflow webserver is using Python: {sys.executable}")
        try:
            conn = BaseHook.get_connection(conn_id='postgres_default')
            logging.warning(f"Connection details: {conn.host}, {conn.login}, {conn.password}")
        except Exception as e:
            logging.error(f"Error fetching connection: {e}")

    @provide_session
    def connect_to_db(session=None):
        try:
            conn_id = 'postgres_default'
            hook = PostgresHook(postgres_conn_id=conn_id)
            logging.warning(f"Attempting to connect to the DB at {hook.get_uri()}")
            connection = hook.get_conn()
            cursor = connection.cursor()
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
            if result:
                logging.warning(f"Query result: {result}")
                logging.warning("Successfully connected to the database!")
            else:
                logging.error("No result from the query.")
            cursor.close()
            connection.close()

        except Exception as e:
            logging.error(f"Error during connection setup or query execution: {e}")

    run_connect_to_db()


prediction_pipeline()

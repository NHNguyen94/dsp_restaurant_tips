import psycopg2
from airflow.utils.session import provide_session


@provide_session
def test_use_postgres_connection(session=None):
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
            print("Successfully connected to the database!")
            print(f"Query result: {result}")
        else:
            print("No result from the query.")
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error during connection setup or query execution: {e}")

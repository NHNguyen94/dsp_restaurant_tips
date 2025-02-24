# To prepare the env
Create conda env with python = 3.9 (The most stable version for airflow)

pip install -r requirements.txt (The airflow inside poetry behaves differently with the airflow installed by pip)

# To init airflow:
export AIRFLOW_HOME=$(pwd)

make init-airflow

make create-admin-airflow

copy content of example_cfg_for_airflow.cfg into airflow.cfg

Update sql_alchemy_conn in airflow.cfg to your db path

# To run airflow:

Note: Because the webserver and scheduler must be run in 2 seperated terminals, so we need to export AIRFLOW_HOME to the pwd in each terminal, otherwise, it will link to root
export AIRFLOW_HOME=$(pwd)

make run-webserver

export AIRFLOW_HOME=$(pwd)

make run-scheduler

Check airflow services: ps aux | grep airflow

Cmd to check and kill conflict ports: 

lsof -i:8080

lsof -i:8793

kill -9 <PID>

dags % airflow tasks run prediction_pipeline connect_to_another_db 2025-02-23

dags % export AIRFLOW_CONFIG=/Users/nguyennguyen/Desktop/github_repos/personal/dsp_restaurant_tips/airflow.cfg
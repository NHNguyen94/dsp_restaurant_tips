# To run airflow:
export AIRFLOW_HOME=$(pwd)

make init-airflow

make create-admin-airflow

copy content of example_cfg_for_airflow.cfg into airflow.cfg

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
# To prepare the env
Create conda env with python = 3.9 (The most stable version for airflow)

pip install -r requirements.txt (The airflow inside poetry behaves differently with the airflow installed by pip)

# To init airflow:

export AIRFLOW_HOME=$(pwd)

Important note: $(pwd) does not work for Linux, you have to pwd first, then copy the absolute path to the command

So it will be like this for Linux users:

pwd

Then copy that absolute path to the command:

export AIRFLOW_HOME=your_absolute_path

After that, you can run the following commands:

make init-airflow

make create-admin-airflow

Then copy the content of example_cfg_for_airflow.cfg into airflow.cfg

Update these env variables in your airflow.cfg:
sql_alchemy_conn: Update it to your airflow.db absolute path
base_log_folder: Update it to your logs folder absolute path
dag_processor_manager_log_location: Update it to your logs/dag_processor_manager/dag_processor_manager.log absolute path
config_file: Update it to your webserver_config absolute path
child_process_log_directory: Update it to your logs/scheduler absolute path


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
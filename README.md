# To prepare the env
Create conda env with python = 3.9 (The most stable version for airflow)

pip install -r requirements.txt (The airflow inside poetry behaves differently with the airflow installed by pip)

# To be able to run full unit tests and the demo, you need to:
- Install docker
- Run `docker compose up` in the project root directory
- Host airflow locally (read below instruction for how)

# To init airflow:

Run `export AIRFLOW_HOME=$(pwd)`

Important note: $(pwd) does not work for Linux, you have to run `pwd` first, then copy the absolute path to the command

So it will be like this for Linux users:

Run `pwd`

Then copy that absolute path to the command:

`export AIRFLOW_HOME=your_absolute_path`

After that, you can run the following commands:

`make init-airflow`

`make create-admin-airflow`

Then copy the content of example_cfg_for_airflow.cfg into airflow.cfg

Update these env variables in your airflow.cfg:
sql_alchemy_conn: Update it to your airflow.db absolute path
base_log_folder: Update it to your logs folder absolute path
dag_processor_manager_log_location: Update it to your logs/dag_processor_manager/dag_processor_manager.log absolute path
config_file: Update it to your webserver_config absolute path
child_process_log_directory: Update it to your logs/scheduler absolute path


# To run airflow:

Note: Because the webserver and scheduler must be run in 2 seperated terminals, so we need to export AIRFLOW_HOME to the pwd in each terminal, otherwise, it will link to root

Run `export AIRFLOW_HOME=$(pwd)`

Note: For Linux users, do this step as the above instruction for init airflow

Run `make run-webserver`

Run `export AIRFLOW_HOME=$(pwd)`

Note: For Linux users, do this step as the above instruction for init airflow

`make run-scheduler`

# If you get the error related to conflict ports, you can use the following commands to check and kill the conflict ports

Check airflow services: Run `ps aux | grep airflow`

Cmd to check and kill conflict ports: 

`lsof -i:8080`

`lsof -i:8793`

`kill -9 <PID>`
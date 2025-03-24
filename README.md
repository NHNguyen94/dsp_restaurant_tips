# To be able to run the demo, you need to:
- Have MacOS or Linux or WSL2 installed on Windows
- For WSL2, you must use the Linux terminal to clone the project and run the commands
- git clone git@github.com:NHNguyen94/dsp_restaurant_tips.git
- Run `cd dsp_restaurant_tips`
- Download this dataset: https://www.kaggle.com/datasets/saurabhbadole/restaurant-tips-dataset
- Copy and rename the train dataset to: src/data/tips.csv
- Install docker
- Create conda env with python = 3.9
- pip install -r requirements.txt
- Install make: `sudo apt update && sudo apt install make` for Linux, and `brew install make` for MacOS
- Run `docker compose up` in the project root directory
- Run `make run-backend` in the project root directory to start the backend
- Run `make run-frontend` in the project root directory to start the frontend
- Run `make split-dataset` or `make split-dataset SPLIT_SIZE=number of files you want to split` This is to split the downloaded kaggle dataset for the ingest pipeline
- Run `make create-false-data` This is to create the false data for the ingest pipeline
- Host airflow locally (read below instruction for how)
- Go to localhost:8080, log in with the credentials admin/admin, and turn on the ingestion_pipeline and prediction_pipeline

# To init and run airflow:
## For MacOS users:
- Run `export AIRFLOW_HOME=$(pwd)`
- Skip the steps to init airflow and create admin if you have already done it, jump to the step to run the webserver
- Run `make init-airflow`
- Run `make create-admin-airflow`
- Then copy the content of example_cfg_for_airflow.cfg into airflow.cfg
- Update these env variables in your airflow.cfg:
    - sql_alchemy_conn: Update it to your airflow.db absolute path
    - base_log_folder: Update it to your logs folder absolute path
    - dag_processor_manager_log_location: Update it to your logs/dag_processor_manager/dag_processor_manager.log absolute path
    - config_file: Update it to your webserver_config absolute path
    - child_process_log_directory: Update it to your logs/scheduler absolute path
- Run `export AIRFLOW_HOME=$(pwd)`
- Run `make run-webserver`
- Open another terminal
- Run `export AIRFLOW_HOME=$(pwd)`
- Run `make run-scheduler`
- If you get the error related to conflict ports, you can use the following commands to check and kill the conflict ports
    - Check airflow services: Run `ps aux | grep airflow`
    - Cmd to check and kill conflict ports: 
        - `lsof -i:8080`
        - `lsof -i:8793`
        - `kill -9 <PID>`, where <PID> is the process id of the conflict port

## For Linux users:
Important note: $(pwd) does not work for Linux, you have to run `pwd` first, then copy the absolute path to the command
- Run `pwd`
- Then copy that absolute path to the command:
- `export AIRFLOW_HOME=your_absolute_path`
- `make init-airflow`
- `make create-admin-airflow`
- Then copy the content of example_cfg_for_airflow.cfg into airflow.cfg
- Update these env variables in your airflow.cfg:
    - sql_alchemy_conn: Update it to your airflow.db absolute path
    - base_log_folder: Update it to your logs folder absolute path
    - dag_processor_manager_log_location: Update it to your logs/dag_processor_manager/dag_processor_manager.log absolute path
    - config_file: Update it to your webserver_config absolute path
    - child_process_log_directory: Update it to your logs/scheduler absolute path
- Run `pwd`
- Then copy that absolute path to the command:
- `export AIRFLOW_HOME=your_absolute_path`
- `make run-webserver`
- Open another terminal
- Run `pwd`
- Then copy that absolute path to the command:
- `export AIRFLOW_HOME=your_absolute_path`
- `make run-scheduler`
- If you get the error related to conflict ports, you can use the following commands to check and kill the conflict ports
    - Check airflow services: Run `ps aux | grep airflow`
    - Cmd to check and kill conflict ports: 
        - `lsof -i:8080`
        - `lsof -i:8793`
        - `kill -9 <PID>`, where <PID> is the process id of the conflict port

# To run the unit tests:
- Run `make unittest`

# To retrain the ML model:
- Run `make pre-process-data`
- Run `make train-model`
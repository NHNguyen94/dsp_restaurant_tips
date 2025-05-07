run-db:
	sudo mkdir -p postgres_data && sudo docker compose up

clear-db:
	docker compose down -v && rm -rf postgres_data

init-airflow:
	 airflow db init

create-admin-airflow:
	airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com

run-webserver:
	airflow webserver --port 8080

run-scheduler:
	airflow scheduler

run-backend:
	PYTHONPATH=. uvicorn src.main:app --reload --port 8000 --log-level debug

run-frontend:
	streamlit run src/app/app.py

split-dataset:
	PYTHONPATH=. python src/services/split_data.py $(SPLIT_SIZE)

# https://stackoverflow.com/questions/2826029/passing-additional-variables-from-command-line-to-make
SPLIT_SIZE ?= 20

create-false-data:
	PYTHONPATH=. python src/services/create_false_data.py

pre-process-data:
	PYTHONPATH=. python src/services/ml_pipelines/pre_processing.py

train-model:
	PYTHONPATH=. python src/services/ml_pipelines/training.py

unittest:
	PYTHONPATH=. pytest -s tests/

format:
	PYTHONPATH=. ruff format

data-for-dashboards:
	PYTHONPATH=. python src/services/create_data_for_dashboards.py
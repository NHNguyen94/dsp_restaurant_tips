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
	PYTHONPATH=. uvicorn src.main:app --reload --port 8000

run-frontend:
	streamlit run src/app/app.py

split-dataset:
	PYTHONPATH=. poetry run python src/services/data_pipelines/split_data.py 25

pre-process-data:
	PYTHONPATH=. python src/services/ml_pipelines/pre_processing.py

train-model:
	PYTHONPATH=. python src/services/ml_pipelines/training.py

unittest:
	PYTHONPATH=. pytest -s tests/

format:
	PYTHONPATH=. ruff format
run-db:
	mkdir -p postgres_data && docker compose up

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
	PYTHONPATH=. poetry run uvicorn src.main:app --reload --port 8000

pre-process-data:
	PYTHONPATH=. poetry run python src/services/ml_pipelines/pre_processing.py

train-model:
	PYTHONPATH=. poetry run python src/services/ml_pipelines/training.py

unittest:
	PYTHONPATH=. poetry run pytest -s tests/

format:
	PYTHONPATH=. ruff format
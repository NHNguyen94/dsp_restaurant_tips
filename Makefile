run-docker:
	mkdir -p postgres_data && docker compose up

clear-docker:
	docker compose down -v

migrate-db:
	PYTHONPATH=. alembic upgrade head

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
run-backend:
	PYTHONPATH=. poetry run uvicorn src.main:app --reload --port 8000

pre-process-data:
	PYTHONPATH=. poetry run python src/ml_pipelines/pre_processing.py

train-model:
	PYTHONPATH=. poetry run python src/ml_pipelines/training.py

unittest:
	PYTHONPATH=. poetry run pytest -s tests/

format:
	PYTHONPATH=. ruff format
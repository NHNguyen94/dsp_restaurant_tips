run-backend:
	PYTHONPATH=. poetry run uvicorn src.main:app --reload --port 8000

unittest:
	PYTHONPATH=. poetry run pytest -s tests/

format:
	PYTHONPATH=. ruff format
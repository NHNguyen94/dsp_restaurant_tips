run-backend:
	PYTHONPATH=. poetry run uvicorn src.main:app --reload --port 8000

unittest:
	PYTHONPATH=. python -m unittest

format:
	PYTHONPATH=. ruff format
# HRMS Lite - Backend (FastAPI)
# Docker: built via root docker-compose (build context: ., dockerfile: Dockerfile)

.PHONY: run install test lint docker-build

# Run backend locally (Poetry + uvicorn)
run:
	poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Install dependencies
install:
	poetry install

# Run tests
test:
	poetry run pytest -v

# Lint
lint:
	poetry run ruff check app/
	poetry run black --check app/

# Build Docker image (same Dockerfile used by root docker-compose)
docker-build:
	docker build -t hrms-backend .

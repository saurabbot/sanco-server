.PHONY: help build up down logs ps shell test lint format alembic-migrate alembic-revision run-local

help:
	@echo "Available commands:"
	@echo "  build            - Build Docker images"
	@echo "  up               - Start all services in Docker"
	@echo "  down             - Stop all services"
	@echo "  logs             - Show Docker logs"
	@echo "  run-local        - Run FastAPI locally (host) with DB in Docker"
	@echo "  migrate          - Run alembic migrations"
	@echo "  revision         - Create a new alembic revision (e.g., make revision m='init')"
	@echo "  test             - Run tests"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

run-local:
	@echo "Starting DB..."
	docker-compose up db -d
	@echo "Waiting for DB..."
	@sleep 3
	@echo "Running App locally..."
	POSTGRES_SERVER=localhost PYTHONPATH=. poetry run uvicorn app.main:app --reload

migrate:
	docker-compose exec app alembic upgrade head

revision:
	docker-compose exec app alembic revision --autogenerate -m "$(m)"

test:
	docker-compose exec app pytest

lint:
	docker-compose exec app black . --check
	docker-compose exec app isort . --check
	docker-compose exec app mypy .

format:
	docker-compose exec app black .
	docker-compose exec app isort .

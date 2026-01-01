# Sanco Server - Scalable FastAPI Boilerplate

This is an extremely scalable FastAPI boilerplate designed for production-ready applications.

## Key Features

- **Redis Chat Memory**: High-performance, IP-based rolling window memory for chatbots.
- **FastAPI**: Modern, fast (high-performance) web framework.
- **SQLAlchemy 2.0 (Async)**: Modern async ORM for database interactions.
- **Alembic**: Database migration management.
- **Pydantic V2**: Fast data validation and core settings management.
- **PostgreSQL**: Robust relational database.
- **Redis**: In-memory data store for sessions and hot context.
- **Docker & Docker Compose**: Containerized development and deployment.
- **Scalable Structure**: Modular architecture (API, Core, DB, Models, Schemas, Services).

## Project Structure

```text
app/
├── api/             # API routes
│   └── api_v1/      # Versioned API
├── core/            # Config, security, logging
├── crud/            # CRUD operations
├── db/              # Database session and base class
├── models/          # SQLAlchemy models
├── schemas/         # Pydantic schemas (DTI/DTO)
├── services/        # Business logic
└── main.py          # Entry point
```

## Getting Started

### 1. Environment Setup

Create a `.env` file in the `sanco_server` directory with the following variables:

```env
PROJECT_NAME="Sanco Server"
SECRET_KEY="your-super-secret-key"
OPENAI_API_KEY="sk-..."

POSTGRES_SERVER=localhost
POSTGRES_PORT=5433
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=app

REDIS_HOST=localhost
REDIS_PORT=6379
```

### 2. Run with Docker (Full Stack)

This will start the DB, Redis, and the FastAPI app in containers:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000/docs`.

### 3. Local Development (Hybrid)

For faster development with hot-reload, run the dependencies in Docker and the app locally:

```bash
# Start DB and Redis
docker-compose up -d db redis

# Install dependencies
poetry install

# Run migrations
PYTHONPATH=. poetry run alembic upgrade head

# Start the server
PYTHONPATH=. poetry run uvicorn app.main:app --reload
```

Or use the provided Makefile:
```bash
make run-local
```

## Database Migrations

Generate a new migration:
```bash
# If running in Docker
docker-compose exec app alembic revision --autogenerate -m "description"

# If running locally
PYTHONPATH=. poetry run alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
# If running in Docker
docker-compose exec app alembic upgrade head

# If running locally
PYTHONPATH=. poetry run alembic upgrade head
```

## Best Practices Implemented

- **Async Database**: All DB operations are non-blocking using `asyncpg`.
- **Dependency Injection**: Database sessions and security are injected using FastAPI's `Depends`.
- **Computed Config**: Database URIs are built dynamically from environment variables.
- **Type Safety**: Extensive use of Python type hints and Pydantic validation.
- **Structure**: Separation of concerns between Models (DB), Schemas (API), and Logic (Services).

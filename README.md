# Sanco Server - Scalable FastAPI Boilerplate

This is an extremely scalable FastAPI boilerplate designed for production-ready applications.

## Key Features

- **FastAPI**: Modern, fast (high-performance) web framework.
- **SQLAlchemy 2.0 (Async)**: Modern async ORM for database interactions.
- **Alembic**: Database migration management.
- **Pydantic V2**: Fast data validation and core settings management.
- **PostgreSQL**: Robust relational database.
- **Docker & Docker Compose**: Containerized development and deployment.
- **JWT Authentication**: Secure token-based authentication (ready to implement).
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

Copy `.env.example` to `.env` and update the values:
```bash
cp .env.example .env
```

### 2. Run with Docker

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000/docs`.

### 3. Database Migrations

Generate a new migration:
```bash
docker-compose exec app alembic revision --autogenerate -m "Initial migration"
```

Apply migrations:
```bash
docker-compose exec app alembic upgrade head
```

## Best Practices Implemented

- **Async Database**: All DB operations are non-blocking using `asyncpg`.
- **Dependency Injection**: Database sessions and security are injected using FastAPI's `Depends`.
- **Computed Config**: Database URIs are built dynamically from environment variables.
- **Type Safety**: Extensive use of Python type hints and Pydantic validation.
- **Structure**: Separation of concerns between Models (DB), Schemas (API), and Logic (Services).

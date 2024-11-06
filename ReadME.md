A production-ready FastAPI application with Design patterns and following best practices in code for managing candidate profiles with secure authentication, CRUD operations, and advanced features.

## Features

- JWT Authentication with secure password hashing
- CRUD operations for candidate management
- Advanced search capabilities with pagination
- Async MongoDB integration
- Celery for background tasks
- Docker containerization
- Comprehensive testing suite
- Error monitoring with Sentry
- Pre-commit hooks for code quality

## Tech Stack

- FastAPI
- Poetry for dependency management
- MongoDB with motor (async driver)
- Pydantic for data validation
- JWT for authentication
- Celery for async tasks
- Docker & Docker Compose
- Pytest for testing
- Sentry for error monitoring

## Installation

1. Clone the repository:
```bash
git clone git@github.com:MirzaBaig715/FastAPI-MongoDB-Candidate-Management.git
cd FastAPI-MongoDB-Candidate-Management
```

2. Copy .env.example to .env and update the values e.g. **_SENTRY_DSN_**:
```bash
cp .env.example .env
```

3. Install dependencies with Poetry:
```bash
poetry install
```

4. Start the services with Docker Compose:
```bash
docker-compose up -d
```

5. Run pre-commit hooks installation:
```bash
poetry run pre-commit install
```

## Development

For running the project locally via terminal.
1. Start the development server:
```bash
poetry run uvicorn src.main:app --reload
```

2. Run tests:
```bash
poetry run pytest
```

3. Access API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

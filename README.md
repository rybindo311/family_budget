# Family Budget Application

A comprehensive family budget management application built with modern technologies.

## 🚀 Tech Stack

- **Backend**: FastAPI, Python 3.12
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Containerization**: Docker, Docker Compose

## 📋 Requirements

- Docker 20.10+
- Docker Compose 2.0+
- Make (optional)

## 🛠️ Installation & Setup

The project uses `make` for convenient deployment and management.



### Production Mode

```bash 
make up
```

### Available Commands

```bash 
make help
```

## 📁 Project Structure

```text
family_budget/
├── backend/
│   ├── alembic.ini           # Alembic configuration
│   ├── Dockerfile            # Production build
│   ├── Dockerfile.dev        # Development build
│   ├── entrypoint.sh         # Container entry point
│   ├── makefile              # Backend-specific commands
│   ├── migrations/           # Database migrations
│   ├── poetry.lock           # Locked dependencies
│   ├── pyproject.toml        # Project dependencies
│   ├── seeds/                # Test data seeds (dev/test only)
│   ├── src/                  # Source code
│   │   ├── config.py         # Application configuration
│   │   ├── database.py       # Database connection
│   │   ├── main.py           # FastAPI application
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── schemas.py        # Pydantic schemas
│   │   └── services.py       # Business logic
│   └── tests/                # Test suite
├── docker-compose.yaml       # Base configuration
├── docker-compose.dev.yaml   # Development override
├── docker-compose.test.yaml  # Testing override
├── makefile                  # Root-level commands
└── README.md                 # This file
```

## 🚦 Environment Modes

The application supports three environment modes:

| Mode | Command | Purpose |
|------|---------|---------|
| Development | `make up-dev` | Local development with hot reload and test data |
| Testing | `make up-test` | Running automated tests |
| Production | `make up` | Optimized production deployment |

## 🌱 Test Data
In development and testing modes, the application automatically seeds the database with:

- Sample families
- Test users
- Sample transactions across different categories

Seeding scripts are located at `backend/seeds/` and run only in dev/test environments.

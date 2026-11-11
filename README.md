python - <<'PY'
from pathlib import Path

Path("README.md").write_text("""# Expense Tracker API

REST API for managing personal expenses, built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- Create expenses
- Get expenses
- Update expenses
- Delete expenses
- Filter expenses by category
- Filter by minimum and maximum amount
- Sort by amount
- Pagination with limit and offset
- Input validation with Pydantic
- Automated tests with pytest
- Isolated SQLite database for tests
- PostgreSQL with Docker
- Environment variables with `.env`
- GitHub Actions CI

## Tech Stack

- Python 3.14
- FastAPI
- SQLAlchemy
- PostgreSQL 16
- Docker
- Pydantic
- Pytest
- GitHub Actions
- Git

## Project Structure

```text
expense_tracker/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   └── models.py
├── tests/
│   ├── conftest.py
│   └── test_expenses.py
├── .github/
│   └── workflows/
│       └── tests.yml
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
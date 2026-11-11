# Expense Tracker API

A REST API for managing personal expenses, built with FastAPI, SQLAlchemy and PostgreSQL.

## Features

- Create expenses
- Get all expenses
- Update expenses
- Delete expenses
- Filter expenses by category
- Filter expenses by minimum amount
- Filter expenses by maximum amount
- Sort expenses by amount
- Pagination with limit and offset
- Input validation with Pydantic
- Automated tests with pytest
- Isolated SQLite database for tests
- PostgreSQL database with Docker

## Tech Stack

- Python 3.14
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- Pytest
- Pydantic
- Git

## Project Structure

```text
expense_tracker/
├── app/
│   ├── main.py
│   ├── database.py
│   └── models.py
├── tests/
│   ├── conftest.py
│   └── test_expenses.py
├── .gitignore
├── README.md
└── docker-compose.yml
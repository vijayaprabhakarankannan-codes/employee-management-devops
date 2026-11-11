
# Employee Management System – DevOps Project

## Project Overview

A full-stack Employee Management System built using Flask,
PostgreSQL, HTML, CSS, and JavaScript.

The project demonstrates Docker containerization, Docker Compose,
automated testing, Git version control, and GitHub Actions CI.

## Technologies Used

- Python 3.12 and Flask
- PostgreSQL 17
- HTML, CSS, and JavaScript
- Docker and Docker Compose
- Git and GitHub
- pytest
- GitHub Actions

## Features

- View employees
- Add employees
- Update employee details
- Delete employees
- Store employee records in PostgreSQL
- Persistent database storage using a Docker volume

## Project Structure

- backend/app.py – Flask application and REST API
- backend/Dockerfile – Docker image instructions
- backend/requirements.txt – Application dependencies
- backend/requirements-test.txt – Testing dependencies
- backend/tests/test_app.py – Automated tests
- frontend/ – User interface
- compose.yaml – Multi-container configuration
- .github/workflows/ci.yml – CI automation
- .dockerignore – Docker build exclusions

## Running Locally

Requirements:
- Docker Desktop
- Docker Compose

Create a `.env` file in the project root:

    DB_PASSWORD=your_local_database_password

For a new database, start the services with:

    docker compose up -d --build

Note: This project currently uses an external Docker volume named
`employee_pgdata`. Create that volume before the first startup
with `docker volume create employee_pgdata`.

Open the application:

    http://127.0.0.1:5002/

## REST API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /employees | Retrieve employees |
| POST | /employees | Create an employee |
| PUT | /employees/{id} | Update an employee |
| DELETE | /employees/{id} | Delete an employee |

## Automated Testing

The project uses pytest to test:

1. Homepage availability
2. GET employee API
3. POST input validation
4. PUT input validation
5. DELETE employee-not-found handling

Tests use mocked database connections where required.

Run locally after installing the Python dependencies:

    python -m pytest backend/tests/test_app.py -v

## GitHub Actions CI

The CI workflow runs on pushes to main and pull requests
targeting main.

Pipeline stages:

1. Checkout source code
2. Set up Python
3. Install dependencies
4. Execute pytest tests
5. Build the Docker image

## Deployment and Monitoring

The application is deployed locally using Docker Compose.

Check running containers:

    docker compose ps

View Flask logs:

    docker compose logs --tail=20 flask

Check API availability:

    curl http://127.0.0.1:5002/employees

## Security Notes

- Database credentials are stored in a Git-ignored .env file.
- Docker build context excludes sensitive local files.
- Flask debug mode is disabled.
- The current setup uses Flask's development server.
  Production deployment requires a production WSGI server,
  HTTPS, and appropriate infrastructure security controls.

## Author

DevOps learning project.

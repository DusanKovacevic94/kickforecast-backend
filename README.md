# KickForecast Backend

This is the backend API for the KickForecast application, built with FastAPI. It provides a CMS for managing content and serves data to the frontend.

## Prerequisites

- Python 3.8+
- PostgreSQL
- [Poetry](https://python-poetry.org/docs/#installation)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd kickforecast-backend
    ```

2.  **Install dependencies:**
    ```bash
    poetry install
    ```

## Configuration

1.  **Environment Variables:**
    Copy the example environment file to create your local configuration:
    ```bash
    cp .env.example .env
    ```

2.  **Update `.env`:**
    Open `.env` and configure the following variables:
    - `DATABASE_URL`: Your PostgreSQL connection string (e.g., `postgresql://user:password@localhost/kickforecast`).
    - `SECRET_KEY`: A secure secret key for JWT tokens.
    - `ALGORITHM`: Encryption algorithm (default: HS256).
    - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time.

## Database

1.  **Run Migrations:**
    Apply the database schema using Alembic:
    ```bash
    poetry run alembic upgrade head
    ```

2.  **Seed Database:**
    Populate the database with initial data:
    ```bash
    poetry run python seed.py
    ```

## Running the Application

Start the development server:

```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.
Interactive API documentation is available at `http://localhost:8000/docs`.

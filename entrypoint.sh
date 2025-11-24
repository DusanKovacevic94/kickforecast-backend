#!/bin/bash
set -e

# Wait for database to be ready (simple sleep for now, or use wait-for-it in production)
echo "Waiting for database..."
sleep 5

# Run migrations
echo "Running migrations..."
alembic upgrade head

# Seed database
echo "Seeding database..."
python seed.py || echo "Seeding failed or already seeded"

# Start application
echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

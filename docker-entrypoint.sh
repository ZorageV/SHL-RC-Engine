#!/bin/bash
set -e

# Wait for the database to be ready (if using a separate database service)
# This is a placeholder - uncomment and modify if needed
# echo "Waiting for database to be ready..."
# while ! nc -z db 5432; do
#   sleep 0.1
# done
# echo "Database is ready!"

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application
echo "Starting the application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 
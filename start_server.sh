set -e

# Run database migrations
alembic upgrade head

# Start your application
uvicorn main:app --host 0.0.0.0

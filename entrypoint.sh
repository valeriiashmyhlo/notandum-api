#!/bin/bash
# entrypoint.sh

# Run database migrations
alembic upgrade head

# Start your application
exec uvicorn main:app --host 0.0.0.0

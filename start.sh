#!/bin/bash
echo "Running database migrations..."
flask db upgrade
echo "Starting gunicorn..."
gunicorn run:app --bind 0.0.0.0:${PORT:-8000}

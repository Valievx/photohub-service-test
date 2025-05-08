#!/bin/env
echo "Waiting for PostgreSQL to start..."
sleep 10
echo "Running migrations..."
python manage.py migrate
echo "Collect static files..."
python manage.py collectstatic --noinput
exec daphne -b 0.0.0.0 -p 8000 src.asgi:application
exec "$@"
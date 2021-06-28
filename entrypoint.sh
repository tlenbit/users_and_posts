#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL started"

poetry run python manage.py makemigrations
poetry run python manage.py migrate

poetry run python manage.py runserver 0.0.0.0:8000

#! /bin/bash

set -e

echo "==> Django setup, executing: collectstatic"
python manage.py collectstatic --noinput

echo "==> Django setup, executing: migrate"
python manage.py migrate

echo "==> Staring wsgi ... "
gunicorn musubiudzetas.wsgi:application --bind :8080 --workers 3
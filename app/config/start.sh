#! /bin/bash

set -e

echo "==> Django setup, executing: collectstatic"
python manage.py collectstatic --noinput

echo "==> Django setup, executing: migrate"
python3 manage.py migrate

echo "==> Staring wsgi ... "
gunicorn musubiudzetas.wsgi --bind 0.0.0.0:8080 --workers 3
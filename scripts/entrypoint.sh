#!/bin/sh

set -e

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database migrations"
python manage.py migrate

uwsgi --socket :8000 --master --enable-threads --module app.wsgi

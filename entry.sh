#!/bin/sh


while ! python manage.py check --database default >/dev/null 2>&1
do
    sleep 2
done

echo "Database is ready."

python manage.py migrate

echo "Collecting static files...."

python manage.py collectstatic --noinput

exec gunicorn jobtracker.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 45
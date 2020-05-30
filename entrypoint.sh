#!/bin/bash

set -e

echo "${0}: running migrations."

python manage.py collectstatic --noinput
python manage.py migrate

gunicorn vier.wsgi -b 0.0.0.0:8000

#!/usr/bin/env bash
# start-server.sh
python manage.py collectstatic
python manage.py migrate
(gunicorn TWT.wsgi --user www-data --bind 0.0.0.0:5000 --workers 3) &
nginx -g "daemon off;"
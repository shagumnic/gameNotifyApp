web: newrelic-admin run-program gunicorn shagumSite.wsgi
worker: celery -A shagumSite worker -B -l info

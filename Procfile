web: newrelic-admin run-program gunicorn shagumSite.wsgi
worker: newrelic-admin run-program celery -A shagumSite worker -B -l info

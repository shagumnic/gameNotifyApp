web: gunicorn shagumSite.wsgi
worker: celery -A shagumSite worker -l info
beat: celery -A shagumSite beat -l info
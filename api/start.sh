python manage.py collectstatic --noinput&&
python manage.py makemigrations&&
python manage.py migrate&&
# uwsgi --ini /var/www/html/api/uwsgi.ini

uwsgi -d --ini /var/www/html/api/uwsgi.ini
celery -A api worker -l info

# nohup background the same as --detach?
# celery -A proj worker --loglevel=INFO --concurrency=10 -n worker1@%h
# celery worker -A app.celery --loglevel=info --detach
# uwsgi -d --ini uwsgi.ini   -d: work in background
# Warnings: if all process working in the background, docker will exit immediately

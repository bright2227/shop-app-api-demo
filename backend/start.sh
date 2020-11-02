python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py runscript factory

#fail
# celery multi start w1 -A proj -l info
# uwsgi --ini /var/www/html/api/uwsgi.ini

uwsgi -d --ini /var/www/html/api/uwsgi.ini
# uwsgi --ini /var/www/html/api/uwsgi.ini
celery -A api worker -l info

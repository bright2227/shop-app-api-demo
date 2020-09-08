from api.deploy import secrets
import os


SECRET_KEY = secrets.SECRET_KEY

ALLOWED_HOSTS = ['*']


#Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0", 
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join( BASE_DIR, 'db.sqlite3'),
    }
}


# celery
broker_url = 'redis://127.0.0.1:6379/0'
result_backend = 'redis://127.0.0.1:6379/0'
accept_content = ["json"]
task_serializer = "json"
result_serializer = "json"
# task_annotations = {'tasks.my_task': {'rate_limit': '10/s'}}
task_time_limit = 10 * 60
task_soft_time_limit = 10 * 60
# beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"


#email
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = secrets.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secrets.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

try:
    from api.deploy import secrets
except:
    from api.deploy import secrets_example as secrets
import os
from api.settings import BASE_DIR


SECRET_KEY = secrets.SECRET_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = secrets.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = secrets.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
SOCIAL_AUTH_FACEBOOK_KEY = secrets.SOCIAL_AUTH_FACEBOOK_KEY
SOCIAL_AUTH_FACEBOOK_SECRET = secrets.SOCIAL_AUTH_FACEBOOK_SECRET

ALLOWED_HOSTS = ['*']
# SITE_URL = 'http://localhost:8000/'
SITE_URL = 'http://localhost/'


# # Database
# # https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'api',
#         'USER': secrets.DATABASE_USER,
#         'PASSWORD': secrets.DATABASE_PASSWORD,
#         'HOST': 'db',
#         'PORT':'3306',
#     }
# }


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Cache
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/0",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#     }
# }


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


# email
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = secrets.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secrets.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

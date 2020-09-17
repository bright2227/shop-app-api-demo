from api.deploy import secrets
import os



SECRET_KEY = secrets.SECRET_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = secrets.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = secrets.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'api', 
        'USER': secrets.DATABASE_USER, 
        'PASSWORD': secrets.DATABASE_PASSWORD, 
        'HOST': 'db', 
        'PORT':'3306', 
    }
}


#Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1", 
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": secrets.CACHES_PASSWORD, 
        },
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHE_TTL = 60 * 1


# celery
broker_url = f"redis://:{secrets.CACHES_PASSWORD}@redis:6379/2"
result_backend = f"redis://:{secrets.CACHES_PASSWORD}@redis:6379/3"
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

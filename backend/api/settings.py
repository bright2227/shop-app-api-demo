"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# debug_mode from docker-compose is string, env file will be prepared later
# DEBUG = bool(int(os.environ.get('debug_mode')))
DEBUG = True
from api.deploy.prod import *
# from api.deploy.dev import *
    

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'debug_toolbar',
    # 'social_django', 'social_core',
    # 'corsheaders',
    # 'django_extensions', # python manage.py reset_db needs turn this on
    'core',
    'django_filters',
    'rest_framework', 
    'drf_yasg',
    'product',
    'order', 'user'
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'social_django.middleware.SocialAuthExceptionMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',
]

# CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'social_django.context_processors.backends',
                # 'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.application'

AUTH_USER_MODEL = "core.User"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

INTERNAL_IPS = [
    '127.0.0.1',
]


# JWT, Filter, Session
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend', ),
}
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}


#swagger
SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': True
}
LOGIN_URL = "api/user/session/login/"
LOGOUT_URL = "api/user/session/logout/"


# Social Oauth
AUTHENTICATION_BACKENDS = (
    # 'social_core.backends.facebook.FacebookOAuth2',
    # 'social_core.backends.github.GithubOAuth2',
    # 'social_core.backends.google.GoogleOAuth2',
    # 'social_core.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)
#final redirct url,  after google send code to /social-auth/complete/google-oauth2/
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_URL_NAMESPACE = 'social'

# key and secrets is imported from secrets
# SOCIAL_AUTH_FACEBOOK_KEY = 
# SOCIAL_AUTH_FACEBOOK_SECRET = 
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']
SOCIAL_AUTH_GOOGLE_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}

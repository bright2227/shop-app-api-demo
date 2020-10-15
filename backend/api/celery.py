from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings  #objects
from django.core.mail import send_mail

# set it in docker-compose
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

app = Celery('celey_mailer')

# if os.environ changes location to below line, autodiscover go wrong
app.config_from_envvar('DJANGO_SETTINGS_MODULE')

# if 'api.settings' changes 'DJANGO_SETTINGS_MODULE', config go wrong
# app.config_from_object('DJANGO_SETTINGS_MODULE', namespace='CELERY')

# OK
# app.config_from_object('api.settings', namespace='CELERY')

# add all tasks in different app, there is no tasks now, not sure it will 
# miss tasks in other apps after adding tasks
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('celery test')
    print('Request: {0!r}'.format(self.request))


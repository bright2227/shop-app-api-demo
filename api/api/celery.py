from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

# if your redis have password
app = Celery('api', broker="redis://:yourpassword@redis:6379/2")

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('celery test')
    # print('Request: {0!r}'.format(self.request))



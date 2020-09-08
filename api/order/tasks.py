import os, time
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_mail_task(recipt, name, email):
    send_mail('receipt',
        recipt,
        'bright2227@gmail.com',
        [email])
    print("mail succeed")
    return None

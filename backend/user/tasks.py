import os, time
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_mail_verify(email_body, email):
    send_mail('Verification mail from shop api',
        email_body,
        'bright2227@gmail.com',
        [email])
    print("verification mail succeed")
    return None


@shared_task
def send_mail_passreset(email_body, email):
    send_mail('Password reset mail from shop api',
        email_body,
        'bright2227@gmail.com',
        [email])
    print("password reset mail succeed")
    return None
    
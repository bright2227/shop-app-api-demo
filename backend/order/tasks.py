from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_mail_order(email_body, email):
    send_mail(
        'Receipt mail from shop api',
        email_body,
        'bright2227@gmail.com',
        [email]
    )
    print("Order receipt mail succeed")
    return None

from home.models import Student
import time
from django.core.mail import send_mail
from django.conf import settings
import smtplib

def send_email_client():
    subject="TEST EMAIL"
    message="Test EMAIL"
    fromEmail = 'kalpnav2015@gmail.com'#settings.EMAIL_HOST_USER
    to_list = ['anoopmonu02@gmail.com']
    send_mail(subject, message, fromEmail, to_list)

#from home.models import Student
import time
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
import smtplib

from django.utils.text import slugify
import uuid

#Send email only
def send_email_client(subject, message, fromEmail, to_list):
    """ subject="TEST EMAIL"
    message="Test EMAIL"
    fromEmail = settings.EMAIL_HOST_USER
    to_list = ['anoopmonu02@gmail.com'] """
    send_mail(subject, message, fromEmail, to_list)

#Send Email with Attachment
def send_email_with_attachment(subject, message, to_list, file_path):
    """ subject="TEST EMAIL SEND FROM DJANGO"
    message="Mail received using django with attachment" """
    fromEmail = settings.EMAIL_HOST_USER
    #to_list = ['anoopmonu02@gmail.com']

    mail = EmailMessage(subject=subject, body=message, from_email=fromEmail, to=to_list)
    mail.attach_file(file_path)
    mail.send()

def generate_slug(title:str)->str:
    from .models import PhoneBook

    """ A function to generate a slug """
    title = slugify(title)

    while(PhoneBook.objects.filter(slug=title).exists()):
        title = f'{slugify(title)}-{str(uuid.uuid4())[:4]}'
    
    return title

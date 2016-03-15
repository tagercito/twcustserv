from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.conf import settings
from customerservice.emailclient import EmailClient

class Command(BaseCommand):

    def handle(self, *args, **options):
        email = EmailMessage('Hello', 'Body goes here', 'ayuda@ticketek.com.ar', ['ayuda@ticketek.com.ar'], headers={'Message-ID': '9'})
        email.send(fail_silently=False)
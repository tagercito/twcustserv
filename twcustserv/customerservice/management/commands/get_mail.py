from django.core.management.base import BaseCommand
import twitter
from django.conf import settings
from customerservice.emailclient import EmailClient

class Command(BaseCommand):

    def handle(self, *args, **options):
        email = EmailClient('ayuda@ticketek.com.ar', 'sentidocomun')
        email.connect()
        emails = email.parse_emails()

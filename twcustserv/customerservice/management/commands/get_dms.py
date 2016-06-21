from django.core.management.base import BaseCommand
from customerservice.models import Contact, Message, CLOSED, OPEN, PENDING
from twitter import Api, TwitterError
import time
from datetime import datetime
from django.conf import settings


api = Api(consumer_key=settings.CONSUMER_KEY,
          consumer_secret=settings.CONSUMER_SECRET,
          access_token_key=settings.ACCESS_TOKEN_KEY,
          access_token_secret=settings.ACCESS_TOKEN_SECRET)


class Command(BaseCommand):

    def handle(self, *args, **options):


        self.screen_name = settings.APPS_TWITTER_USERNAME
        #TwitterAPI jamas trae tus propios DirectMessages, trae solo incoming.
        for msg in api.GetDirectMessages(self.screen_name):
            if msg.sender_screen_name != self.screen_name:
                date_created = datetime.strptime(
                    msg.created_at,
                    '%a %b %d %H:%M:%S %z %Y'
                )
                contact, created = Contact.objects.get_or_create(
                    user_id=msg.sender_id,
                    screen_name=msg.sender_screen_name,
                    type=Contact.THREAD,
                    defaults={
                        'created': date_created
                    })
                if created or contact.status == Contact.CLOSED:
                    try:
                        own_msg = api.PostDirectMessage(
                            settings.ANSWER_TO_DIRECT_MESSAGE % msg.sender_screen_name, msg.sender_id
                        )
                        msg_data = {
                            "creator": True,
                            "contact": contact,
                            "message_id": own_msg.id,
                            "sender": own_msg.sender_id,
                            "message": own_msg.text
                        }
                        message, created = Message.objects.get_or_create(**msg_data)
                        contact.status = Contact.OPEN
                        contact.save()
                    except (TwitterError) as e:
                        pass
                msg_data = {
                    "creator": True,
                    "contact": contact,
                    "message_id": msg.id,
                    "sender": msg.sender_id,
                    "message": msg.text
                }
                message, created = Message.objects.get_or_create(**msg_data)

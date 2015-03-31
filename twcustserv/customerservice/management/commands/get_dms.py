from django.core.management.base import BaseCommand
from customerservice.models import Thread, Message 


#Base application to get DirectMessages from Twitter API
import twitter
import time
from django.conf import settings
api = settings.TWITTER_API_CREDENTIALS



class Command(BaseCommand):
			
	def handle(self, *args, **options):


		self.screen_name = 'apimtechtest'
		#TwitterAPI jamas trae tus propios DirectMessages, trae solo incoming.
		for msg in api.GetDirectMessages(self.screen_name):
			thread, created = Thread.objects.get_or_create(user_id = msg.GetSenderId(),screen_name=msg.sender_screen_name, defaults={'date_created': time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(msg.created_at,'%a %b %d %H:%M:%S +0000 %Y'))})
			if created or thread.status=CLOSED:
				own_msg = api.PostDirectMessage('texto de testeessssssssss', msg.GetSenderId())
				message, created = Message.objects.get_or_create(creator=True,thread=thread,message_id=own_msg.id, sender=own_msg.sender_id, message= own_msg.text)
				thread.status = OPEN
				thread.save()
			message, created = Message.objects.get_or_create(creator=True,thread=thread,message_id=msg.id, sender=msg.sender_id, message= msg.text)

	


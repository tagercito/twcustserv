from django.core.management.base import BaseCommand
from customerservice.models import Thread, Message 
#Base application to get DirectMessages from Twitter API
import twitter
import time
class Command(BaseCommand):
			
	def handle(self, *args, **options):
		#estos valores van el settings.

		api = twitter.Api(consumer_key='Fbve1E4JqZ0cnb9ouVoOycbgp',
				  consumer_secret='2HOEHzTR2E6LAbWmglkFwOzq2WCZ3X2LJwguHFq0eUVZIWNmRX', 
				  access_token_key='3129661635-wjyM6RYKSWQ37LDhNOtmvDmNNq0JkL1n1SI75EJ', 
				  access_token_secret='vnDCKDf1ILaZMuJaTgO4cvaFdFr3oP7AXMsBanblyLU84')

		self.screen_name = 'apimtechtest'
		#TwitterAPI jamas trae tus propios DirectMessages, trae solo incoming.
		for msg in api.GetDirectMessages(self.screen_name):
			thread, created = Thread.objects.get_or_create(user_id = msg.GetSenderId(),screen_name=msg.sender_screen_name, defaults={'date_created': time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(msg.created_at,'%a %b %d %H:%M:%S +0000 %Y'))})
			if created or thread.status:
				own_msg = api.PostDirectMessage('texto de testeessssssssssee', msg.GetSenderId())
				message, created = Message.objects.get_or_create(creator=True,thread=thread,message_id=own_msg.id, sender=own_msg.sender_id, message= own_msg.text)
				thread.status = False
				thread.save()
			message, created = Message.objects.get_or_create(creator=True,thread=thread,message_id=msg.id, sender=msg.sender_id, message= msg.text)

	


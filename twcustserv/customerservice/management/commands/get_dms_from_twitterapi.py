from django.core.management.base import BaseCommand
from customerservice.models import Thread, Message 
#Base application to get DirectMessages from Twitter API
import twitter
import time
class Command(BaseCommand):
			
	def handle(self, *args, **options):
		#estos valores van el settings.

		api = twitter.Api(consumer_key='SJfHGWO9saCQAYvLLbTmX3CJQ',
				  consumer_secret='j3ilbC5Nn7Pgug89wi1sQNpkAcKYcJ4U2ZdcJ18yrvlRdkZ6te', 
				  access_token_key='30598040-kKdSKjnFWgS6h1L54ge3k4OKn2sTKYaWy4Qa3ARIn', 
				  access_token_secret='c6iGAdcht4iACPJw7BBEMgOB3mnkIzNRSPlJx0ZdgxRrD')

		self.screen_name = 'cgalceran'
		#TwitterAPI jamas trae tus propios DirectMessages, trae solo incoming.
		for msg in api.GetDirectMessages(self.screen_name):
			thread, created = Thread.objects.get_or_create(screen_name=msg.sender_screen_name,
														   date_created=time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(msg.created_at,'%a %b %d %H:%M:%S +0000 %Y')))
			message, created = Message.objects.get_or_create(thread=thread,message_id=msg.id, sender=msg.sender_id, message= msg.text)

	


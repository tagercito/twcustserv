from django.core.management.base import BaseCommand
from customerservice.models import Thread, Message 
import twitter
import time
class Command(BaseCommand):
			
	def handle(self, *args, **options):

		api = twitter.Api(consumer_key='SJfHGWO9saCQAYvLLbTmX3CJQ',
				  consumer_secret='j3ilbC5Nn7Pgug89wi1sQNpkAcKYcJ4U2ZdcJ18yrvlRdkZ6te', 
				  access_token_key='30598040-kKdSKjnFWgS6h1L54ge3k4OKn2sTKYaWy4Qa3ARIn', 
				  access_token_secret='c6iGAdcht4iACPJw7BBEMgOB3mnkIzNRSPlJx0ZdgxRrD')
		self.screen_name = 'cgalceran'
		friend_ids = api.GetFriendIDs()
		for mention in api.GetMentions():
			api.PostUpdate('Hola @%s, por favor mandanos mensaje directo' % mention.user.screen_name,
						 	mention.id)				
 			if mention.user.id not in friend_ids:
 				api.CreateFriendship(mention.user)
				#dm_text = "Hola, pasanos por aca tus datos privados"
				#api.PostDirectMessage(mention.user)
				
				#print ' no es amigo %s' % mention.user.screen_name
from django.core.management.base import BaseCommand
from customerservice.models import Thread, Message 
import twitter
import time
class Command(BaseCommand):
			
	def handle(self, *args, **options):

		api = twitter.Api(consumer_key='Fbve1E4JqZ0cnb9ouVoOycbgp',
				  consumer_secret='2HOEHzTR2E6LAbWmglkFwOzq2WCZ3X2LJwguHFq0eUVZIWNmRX', 
				  access_token_key='3129661635-wjyM6RYKSWQ37LDhNOtmvDmNNq0JkL1n1SI75EJ', 
				  access_token_secret='vnDCKDf1ILaZMuJaTgO4cvaFdFr3oP7AXMsBanblyLU84')
		self.screen_name = 'apimtechtest'
		friend_ids = api.GetFriendIDs()
		for mention in api.GetMentions():
			api.PostUpdate('Hola @%s, por favor mandanos mensaje directo' % mention.user.screen_name,
						 	mention.id)				
 			if mention.user.id not in friend_ids:
 				api.CreateFriendship(mention.user)
				#dm_text = "Hola, pasanos por aca tus datos privados"
				#api.PostDirectMessage(mention.user)
				
				#print ' no es amigo %s' % mention.user.screen_name
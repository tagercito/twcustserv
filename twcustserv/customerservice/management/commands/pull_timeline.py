from django.core.management.base import BaseCommand
from customerservice.models import Thread, Message 
import twitter
import time
from django.conf import settings
api = settings.TWITTER_API_CREDENTIALS 

class Command(BaseCommand):
			
	def handle(self, *args, **options):

		self.screen_name = 'apimtechtest'
		
		friend_ids = api.GetFriendIDs()
		
		for mention in api.GetMentions():
			api.PostUpdate('Hola @%s, por favor mandanos un mensaje directo con tus datos y una descripcion del problema' % mention.user.screen_name,
						 	mention.id)	#tira error por duplicar  "leer 3er parrafo https://dev.twitter.com/rest/reference/post/statuses/update"			
 			if mention.user.id not in friend_ids:
 				api.CreateFriendship(mention.user.id)


				
from django.core.management.base import BaseCommand
from customerservice.models import Thread, Message 
import twitter
import time
from django.conf import settings

#TWITTER_API_CREDENTIALS = (consumer_key=settings.CONSUMER_KEY, consumer_secret=settings.CONSUMER_SECRET, access_token_key=settings.ACCESS_TOKEN_KEY, access_token_secret=settings.ACCESS_TOKEN_SECRET)

api = twitter.Api(consumer_key=settings.CONSUMER_KEY, consumer_secret=settings.CONSUMER_SECRET, access_token_key=settings.ACCESS_TOKEN_KEY, access_token_secret=settings.ACCESS_TOKEN_SECRET) 

class Command(BaseCommand):
			
	def handle(self, *args, **options):
		
		self.screen_name = settings.APPS_TWITTER_USERNAME
		
		friend_ids = api.GetFriendIDs()
		for mention in api.GetMentions():
			api.PostUpdate(settings.POST_MENTION_UPDATE % mention.user.screen_name, mention.id)	#tira error por duplicar  "leer 3er parrafo https://dev.twitter.com/rest/reference/post/statuses/update"			
 			if mention.user.id not in friend_ids:
 				api.CreateFriendship(mention.user.id)

				
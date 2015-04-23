from django.core.management.base import BaseCommand
import twitter
from django.conf import settings

api = twitter.Api(consumer_key=settings.CONSUMER_KEY, consumer_secret=settings.CONSUMER_SECRET,
                  access_token_key=settings.ACCESS_TOKEN_KEY, access_token_secret=settings.ACCESS_TOKEN_SECRET)


class Command(BaseCommand):

    def handle(self, *args, **options):

        friend_ids = api.GetFriendIDs()
        for mention in api.GetMentions():
            if mention.text.startswith('@'+settings.APPS_TWITTER_USERNAME):      
                try:
                    api.PostUpdate(settings.POST_MENTION_UPDATE % mention.user.screen_name, mention.id)
                except:
                    continue
                else:
                    if mention.user.id not in friend_ids:
                        api.CreateFriendship(mention.user.id)

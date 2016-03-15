from django.core.management.base import BaseCommand
import twitter
from django.conf import settings
from customerservice.models import Pull
api = twitter.Api(consumer_key=settings.CONSUMER_KEY, consumer_secret=settings.CONSUMER_SECRET,
                  access_token_key=settings.ACCESS_TOKEN_KEY, access_token_secret=settings.ACCESS_TOKEN_SECRET)


class Command(BaseCommand):

    def get_last_message_id(self):
        try:
            last_pull = Pull.objects.all().order_by('-date')[0]
        except:
            pass
        else:
            return last_pull.message_id

    def get_mentions(self):
        last_id = self.get_last_message_id()
        if last_id:
            return api.GetMentions(since_id=last_id)
        return api.GetMentions()

    def update_pull(self, mention_id):
        Pull.objects.create(message_id=mention_id)

    def handle(self, *args, **options):
        last_mention_id = None
        friend_ids = api.GetFriendIDs()
        for mention in self.get_mentions():
            if mention.text.startswith('@'+settings.APPS_TWITTER_USERNAME):      
                try:
                    api.PostUpdate(settings.POST_MENTION_UPDATE % mention.user.screen_name, mention.id)
                except:
                    continue
                else:
                    if mention.user.id not in friend_ids:
                        api.CreateFriendship(mention.user.id)
            last_mention_id = mention.id
        if last_mention_id:
            self.update_pull(last_mention_id)

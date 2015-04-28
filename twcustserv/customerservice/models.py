from django.db import models
from django.db.models.signals import post_save
import twitter
from django.conf import settings

api = twitter.Api(consumer_key=settings.CONSUMER_KEY, consumer_secret=settings.CONSUMER_SECRET, access_token_key=settings.ACCESS_TOKEN_KEY, access_token_secret=settings.ACCESS_TOKEN_SECRET)  


#create a choice field inside the class
OPEN = 'OP'
PENDING = 'PE'       
CLOSED = 'CL' 

TICKET_STATUS_CHOICES = (
    (OPEN,'Open'),
    (PENDING,'Pending'),
    (CLOSED,'Closed'),
)



class Thread(models.Model):
    screen_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=140)
    date_created = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=TICKET_STATUS_CHOICES, default=OPEN)
    assigned_to = models.ForeignKey('auth.User', null=True, blank=True )
    
    def __unicode__(self):
        return self.screen_name

class Message(models.Model):
    creator = models.BooleanField(default=False)
    thread = models.ForeignKey(Thread)
    message = models.TextField()
    sender = models.CharField(max_length=140, null=True, blank=True)
    message_id = models.CharField(max_length=20, null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', null=True, blank=True)

    def __unicode__(self):
        return self.message_id if self.message_id else ''


class Bulletin(models.Model):
    user = models.ForeignKey('auth.User', null=True, blank=True)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    important = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s-%s' % (self.user, self.important)


class Pull(models.Model):
    date = models.DateTimeField(auto_now=True)
    message_id = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s - %s' % (str(self.date), str(self.message_id))

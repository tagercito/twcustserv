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

def split(s, l=[]): #funcion recursiva que parte el texto en strings de 140 caracteres
    if len(s) < 140:
        l.append(s)
        return l
    l.append(s[:140-len(settings.CONTINUA)]+settings.CONTINUA)
    return split(s[140-len(settings.CONTINUA):], l)


class Thread(models.Model):
    screen_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=140)
    date_created = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=TICKET_STATUS_CHOICES, default=OPEN)
    #assigned_to = models.ForeignKey('auth.User')
    
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

def post_msg_to_twitter(sender, instance, created, **kwargs):
    own_msg = None
    if not instance.creator:
        for message in split(instance.message):
            try:
                own_msg = api.PostDirectMessage(message, instance.thread.user_id)
            except:
                pass
        if own_msg:
            instance.message_id = str(own_msg.id)
            instance.creator = True
            instance.save()

post_save.connect(post_msg_to_twitter, sender=Message)


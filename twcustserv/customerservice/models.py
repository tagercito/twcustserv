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

# Create your models here.

def split(s, l=[]): #funcion recursiva que parte el texto en strings de 140 caracteres
  l.append(s[:140-len(settings.CONTINUA)]+settings.CONTINUA)
  if len(s) < 140:return l
  return split(s[140-len(settings.CONTINUA):], l)


class Thread(models.Model):
       screen_name = models.CharField(max_length=100)
       user_id = models.CharField(max_length=140)
       date_created = models.DateTimeField(auto_now=True)
       status = models.CharField(max_length=2,choices=TICKET_STATUS_CHOICES,default=OPEN)

       def __unicode__(self):
       	return self.screen_name

class Message(models.Model):
       creator = models.BooleanField(default=False)
       thread = models.ForeignKey(Thread)
       message = models.TextField()
       sender = models.CharField(max_length=140, null=True, blank=True)
       message_id = models.CharField(max_length=20, null=True,blank=True)

       def __unicode__(self):
       	return self.message_id



def post_msg_to_twitter(sender, instance, created, **kwargs):
       
       if not instance.creator:              
              for message in split(instance.message):
                  own_msg = api.PostDirectMessage(message, instance.thread.user_id)
              instance.message_id = str(own_msg.id) 
              instance.creator= True
              instance.save()

post_save.connect(post_msg_to_twitter, sender=Message)


from django.db import models
from django.db.models.signals import post_save
import twitter

# Create your models here.


class Thread(models.Model):
       screen_name = models.CharField(max_length=100)
       user_id = models.CharField(max_length=140)
       date_created = models.DateTimeField(auto_now=True)

       status = models.BooleanField(default=False)

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

def split(s, l):
  l.append(s[:139])
  if len(s) < 140:return l
  return split(s[139:], l)

def post_msg_to_twitter(sender, instance, created, **kwargs):
       if not instance.creator:
              api = twitter.Api(consumer_key='SJfHGWO9saCQAYvLLbTmX3CJQ',
                              consumer_secret='j3ilbC5Nn7Pgug89wi1sQNpkAcKYcJ4U2ZdcJ18yrvlRdkZ6te', 
                              access_token_key='30598040-kKdSKjnFWgS6h1L54ge3k4OKn2sTKYaWy4Qa3ARIn', 
                              access_token_secret='c6iGAdcht4iACPJw7BBEMgOB3mnkIzNRSPlJx0ZdgxRrD')
              for message in split(instance.message,[]):
                     print len(message)
                     own_msg = api.PostDirectMessage(message, instance.thread.user_id)
              #Agregar logica de recortar el texto en 140 caracteres
              instance.message_id = str(own_msg.id) 
              instance.creator= True
              instance.save()

post_save.connect(post_msg_to_twitter, sender=Message)

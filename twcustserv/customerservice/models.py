from django.db import models
from django.db.models.signals import post_save
import twitter
from django.conf import settings

api = settings.TWITTER_API_CREDENTIALS 

# Create your models here.


class Thread(models.Model):
       screen_name = models.CharField(max_length=100)
       user_id = models.CharField(max_length=140)
       date_created = models.DateTimeField(auto_now=True)
       
       #create a choice field inside the class
       OPEN = 'OP'
       PENDING = 'PE'       
       CLOSED = 'CL'
       TICKET_STATUS_CHOICES = (
        (OPEN,'Open'),
        (PENDING,'Pending'),
        (CLOSED,'Closed'),
        )
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


#funcion recursiva que parte el texto en strings de 130 caracteres
def split(s, l): 
  l.append(s[:130])
  if len(s) < 140:return l
  return split(s[130:], l)

continua=' (cont)'

def post_msg_to_twitter(sender, instance, created, **kwargs):
       if not instance.creator:
              
              for message in split(instance.message,[]):
                if message != split(instance.message,[])[-1]: #logica para agregar (' cont') en todos menos el ultimo mensaje 
                  own_msg = api.PostDirectMessage(message+continua, instance.thread.user_id)
                else:
                  own_msg = api.PostDirectMessage(message, instance.thread.user_id)
              instance.message_id = str(own_msg.id) 
              instance.creator= True
              instance.save()

post_save.connect(post_msg_to_twitter, sender=Message)


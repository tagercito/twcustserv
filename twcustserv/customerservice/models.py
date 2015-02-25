from django.db import models

# Create your models here.


class Thread(models.Model):
       screen_name = models.CharField(max_length=100)
       date_created = models.DateTimeField(auto_now=True)

class Message(models.Model):
       thread = models.ForeignKey(Thread)
       message = models.CharField(max_length=140)
       sender = models.CharField(max_length=140)
       message_id = models.CharField(max_length=20)
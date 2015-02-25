from django.core.management.base import BaseCommand, CommandError
from CustomerService.models import Thread, Message 


#Base application to get DirectMessages from Twitter API

import twitter

api = twitter.Api(consumer_key='SJfHGWO9saCQAYvLLbTmX3CJQ',
				  consumer_secret='j3ilbC5Nn7Pgug89wi1sQNpkAcKYcJ4U2ZdcJ18yrvlRdkZ6te', 
				  access_token_key='30598040-kKdSKjnFWgS6h1L54ge3k4OKn2sTKYaWy4Qa3ARIn', 
				  access_token_secret='c6iGAdcht4iACPJw7BBEMgOB3mnkIzNRSPlJx0ZdgxRrD')

		

#Management Command

class Command(BaseCommand):
			
	def handle(self):

		def getdirectmessages():
			""" Funcion para obtener los ultimos 20 mensajes directos de una cuenta de twitter"""
			#TwitterAPI jamas trae tus propios DirectMessages, trae solo incoming.
			dms = api.GetDirectMessages('cgalceran')

			for msg in dms:
				add_messages(message_id=msg.id,sender_id=msg.sender_id,messagetext=msg.text)
				add_threads(sender_screen_name=msg.sender_screen_name,date_created=msg.created_at)
							
		def add_messages(message_id, sender_id, messagetext):
			"Metodo para insertar la data en la tabla de Messages"
			m = Message.objects.get_or_create(message_id=message_id, sender=sender_id, message= messagetext)
			return m

		def add_threads(sender_screen_name, date_created):
			"Metodo para insertar la data en la tabla de Thread"
			t = Thread.objects.get_or_create(screen_name=sender_screen_name, date_created=date_created)
			return t
	
		


import twitter
from django.conf import settings


api = twitter.Api(consumer_key='Fbve1E4JqZ0cnb9ouVoOycbgp',
				  consumer_secret='2HOEHzTR2E6LAbWmglkFwOzq2WCZ3X2LJwguHFq0eUVZIWNmRX', 
				  access_token_key='3129661635-wjyM6RYKSWQ37LDhNOtmvDmNNq0JkL1n1SI75EJ', 
				  access_token_secret='vnDCKDf1ILaZMuJaTgO4cvaFdFr3oP7AXMsBanblyLU84')


mentions = api.GetMentions()

message_id=[]
date_created=[]
sender_id=[]
sender_screen_name=[]
messagetext =[]

print mentions

for msg in mentions:
	
	message_id.append(msg.id)
	date_created.append(msg.created_at)
	#sender_id.append(msg.sender_id)
	#sender_screen_name.append(msg.sender_screen_name)
	messagetext.append(msg.text)

print (message_id, messagetext)

#Felizzzzz hookeado al twitterAPI por primera vez...

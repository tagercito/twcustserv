
import twitter

api = twitter.Api(consumer_key='SJfHGWO9saCQAYvLLbTmX3CJQ',
				  consumer_secret='j3ilbC5Nn7Pgug89wi1sQNpkAcKYcJ4U2ZdcJ18yrvlRdkZ6te', 
				  access_token_key='30598040-kKdSKjnFWgS6h1L54ge3k4OKn2sTKYaWy4Qa3ARIn', 
				  access_token_secret='c6iGAdcht4iACPJw7BBEMgOB3mnkIzNRSPlJx0ZdgxRrD')

dms = api.GetDirectMessages('cgalceran')

message_id=[]
date_created=[]
sender_id=[]
sender_screen_name=[]
messagetext =[]

for msg in dms:
	message_id.append(msg.id)
	date_created.append(msg.created_at)
	sender_id.append(msg.sender_id)
	sender_screen_name.append(msg.sender_screen_name)
	messagetext.append(msg.text)


print (message_id)

#Felizzzzz hookeado al twitterAPI por primera vez...
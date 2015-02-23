
import twitter

api = twitter.Api(consumer_key='SJfHGWO9saCQAYvLLbTmX3CJQ',
				  consumer_secret='j3ilbC5Nn7Pgug89wi1sQNpkAcKYcJ4U2ZdcJ18yrvlRdkZ6te', 
				  access_token_key='30598040-kKdSKjnFWgS6h1L54ge3k4OKn2sTKYaWy4Qa3ARIn', 
				  access_token_secret='c6iGAdcht4iACPJw7BBEMgOB3mnkIzNRSPlJx0ZdgxRrD')

dms = api.GetDirectMessages('cgalceran')

print [msg.text for msg in dms]

#Felizzzzz hookeado al twitterAPI por primera vez...
from secret import *
import tweepy
from random import choice

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

class BotStreamer(tweepy.StreamListener):
	def on_status(self, status):
		username = status.user.screen_name
		status_id = status.id

		if 'ping' in status.text.lower():
			tweet = "@" + status.user.screen_name + " pong"
			api.update_status(status = tweet, in_reply_to_status_id = status_id)

		if 'shiba' in status.text.lower():
			pictureList = ["shiba/1.jpg", "shiba/2.jpg", "shiba/3.jpg", "shiba/4.jpg", "shiba/5.jpg", "shiba/6.jpg", 
			"shiba/7.jpg", "shiba/8.jpg", "shiba/9.jpg", "shiba/10.jpg", ]
			tweetPicutre = "@" + status.user.screen_name
			api.update_with_media(filename=choice(pictureList), status=tweetPicutre, in_reply_to_status_id = status_id)

myStreamListener = BotStreamer()
stream = tweepy.Stream(auth, myStreamListener)
stream.filter(track=['@Bot_Harajuku'])
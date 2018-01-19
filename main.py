from secret import *
import tweepy
from random import choice
import os
from lib.googleImagesDownload import *
import shutil

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
			downloadSingleImage("shiba+inu")
			tweetPicture = "@" + status.user.screen_name
			picturePath = "shiba+inu/" + choice(os.listdir("shiba+inu"))
			api.update_with_media(filename=picturePath, status=tweetPicture, in_reply_to_status_id = status_id)
			shutil.rmtree("shiba+inu", ignore_errors=True)

myStreamListener = BotStreamer()
stream = tweepy.Stream(auth, myStreamListener)
stream.filter(track=['@Bot_Harajuku'])
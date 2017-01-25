# Hackathon Project 25/01/17
# Jamie Luckett, Lucy Firman and James McCartney

import tweepy
import config
import json
from tweepy.streaming import StreamListener

def getAuth():
    auth = tweepy.OAuthHandler(config.getApiKey(), config.getApiSecret())
    auth.set_access_token(config.getAccessToken(),config.getAccessSecret())

    return auth

def createStream(Username):
    auth = getAuth()
    streamListener = tweepy.Stream(auth = auth, listener=MyListener())
    streamListener.filter(track=[config.getBotUsername()])

class MyListener(StreamListener):
    def on_data(self, data):
        decoded = json.loads(data)
        entities = decoded['entities']
        userMentions = entities['user_mentions']
        for userMention in userMentions:
            if userMention['screen_name'] != config.getBotUsername():
                print(userMention['screen_name'])
                # Its not us, do something with it..
                # TODO: Call markov chain and tweet


# Hackathon Project 25/01/17
# Jamie Luckett, Lucy Firman and James McCartney

import tweepy
import config

def getAuth():
    auth = tweepy.OAuthHandler(config.getApiKey(), config.getApiSecret())
    auth.set_access_token(config.getAccessToken(),config.getAccessSecret())

    return auth

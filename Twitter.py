# Hackathon Project 25/01/17
# Jamie Luckett, Lucy Firman and James McCartney

import tweepy
import config
import json
import os
import re
import random
from time import strftime

import markov, auth
import tweet as tweeter

TWEET_LENGTH = 140
LOG_FILE = "past tweets.txt"

class MyListener(tweepy.StreamListener):
    def on_data(self, data):
        decoded = json.loads(data)
        entities = decoded['entities']
        userMentions = entities['user_mentions']
        for userMention in userMentions:
            if userMention['screen_name'] != config.getBotUsername():
                print(userMention['screen_name'])
                # Its not us, do something with it..
                markovAndTweet(userMention['screen_name'])

    def on_error(self, status_code):
        if status_code == 420:
            # We are being rate limited by Twitter =(
            # Disconnect from the stream
            return False
        else:
            # Any other error, return true to keep the stream open
            return True

def createStream(Username):
    streamListener = tweepy.Stream(auth.getAuth(), MyListener())
    streamListener.filter(track=[config.getBotUsername()])

def grabUserTweets(Username, CheckFor200 = True):
    # TODO: Fix!! If a user does not have >= 200 non RT tweets this will endlessly loop and probabaly end the world
    returnTweets = {}
    api = tweepy.API(getAuth())
    tweets = api.user_timeline(screen_name=Username, count=200)
    for tweet in tweets:
        if not tweet.text.startswith("RT") :
            returnTweets[tweet.id] = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet.text)

    if CheckFor200:
        while len(returnTweets) <= 200:
            lastID = tweets[-1].id
            print(lastID)
            tweets = api.user_timeline(screen_name=Username, count=200, start_id=lastID)
            for tweet in tweets:
                if not tweet.text.startswith("RT"):

                    returnTweets[tweet.id] = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet.text)
        else:
            return returnTweets
    return returnTweets

def saveTweets(Username):
    if not os.path.isdir("data/"):
        os.makedirs('data/')
    if os.path.isfile('data/'+Username+'.json'):
        # Database already exists, read it in and add to it
        with open('data/'+Username+'.json') as jsonIn:
            oldTweets = json.load(jsonIn)
            return oldTweets
    else:
        with open("data/"+Username+".json", 'w') as jsonOut:
            tweets = grabUserTweets(Username, False)
            json.dump(tweets, jsonOut)
            return tweets

def saveMarkovTuples(Username, Tweets):
    tuples = []
    for tweet in Tweets:
        tweetsplit = Tweets[tweet].split(" ")

        for i in range(len(tweetsplit) - 1):
            tuples.append((tweetsplit[i], tweetsplit[i + 1]))

    with open("data/" + Username + ".tuples.json", 'w') as jsonOut:
        json.dump(tuples, jsonOut)
        return tuples

def markovAndTweet(Username):
    '''Prepares markov tuples and passes to markov chain method'''
    chain = saveMarkovTuples(Username,saveTweets(Username))
    prefix = Username + " - " 
    toTweet = markov.buildChain(chain, len(prefix))
    tweeter.tweetString(prefix + toTweet)

if __name__ == "__main__":
    print("BarkovChain Initialized on", strftime("%d/%m/%Y"), "@", strftime("%H:%M:%S"))
    createStream(config.getBotUsername())

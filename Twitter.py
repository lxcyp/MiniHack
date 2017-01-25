# Hackathon Project 25/01/17
# Jamie Luckett, Lucy Firman and James McCartney

import tweepy
import config
import json
import os
import re
import random


TWEET_LENGTH = 140
LOG_FILE = "past tweets.txt"


def getAuth():
    auth = tweepy.OAuthHandler(config.getApiKey(), config.getApiSecret())
    auth.set_access_token(config.getAccessToken(),config.getAccessSecret())

    return auth

def createStream(Username):
    auth = getAuth()
    streamListener = tweepy.Stream(auth = auth, listener=MyListener())
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
            print("fuck")
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

def buildChain(markov_array):
    TWEET_MAX = 140
    current_tweet = ""
    finished_tweet = False
    first_tuple = random.choice(markov_array)
    current_tweet += first_tuple[0]
    next_word = first_tuple[1]
    start_word = next_word

    while not finished_tweet:
        finished_tweet = True
        next_word = findWord(start_word, markov_array)
        if len(current_tweet) + len(next_word) + 1 < 140:
            finished_tweet = False
            current_tweet = current_tweet + " " + next_word
            start_word = next_word

    tweetString(current_tweet)


def findWord(last_word, markov_array):
    candidate_words = []
    for i in markov_array:
        if i[0] == last_word:
            candidate_words.append(i[1])

    if len(candidate_words) == 0:
        return " "
    else:
        return random.choice(candidate_words)



def markovAndTweet(Username):
    '''
    Prepares markov tuples and passes to markov chain method
    '''
    # TODO: Pass to Lucy's markov chain
    chain = saveMarkovTuples(Username,saveTweets(Username))
    buildChain(chain)



class MyListener(tweepy.StreamListener):
    def on_data(self, data):
        decoded = json.loads(data)
        entities = decoded['entities']
        userMentions = entities['user_mentions']
        for userMention in userMentions:
            if userMention['screen_name'] != config.getBotUsername():
                print(userMention['screen_name'])
                # Its not us, do something with it..
                # TODO: Call markov chain and tweet
                markovAndTweet(userMention['screen_name'])



auth = getAuth()

def tweetString(tweet):
    tweet = stripTweet(tweet)
    """Takes a string and tweets it"""
    if len(tweet) > TWEET_LENGTH:
        print("Tweet length greater than", TWEET_LENGTH)

    elif len(tweet) == 0:
        print("Tweet length is 0")

    else:
        print("Tweeting:", tweet)
        try:
            api = tweepy.API(auth)
            api.update_status(tweet)
            logTweet(tweet)
        except Exception as e:
            print("Tweet failed")
            print(str(e))

def stripTweet(tweet):
    """Removes @ symbols from tweets"""
    return tweet.replace('@', '')

def logTweet(tweet):
    """Logs tweet to LOG_FILE"""
    file = open(LOG_FILE, 'a')
    file.write(tweet + "\n")
    file.close()


#tweets = grabUserTweets('JimJam707',False)
#markovAndTweet('realDonaldTrump')

createStream(config.getBotUsername())

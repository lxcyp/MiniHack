# Hackathon Project 25/01/17
# Jamie Luckett, Lucy Firman and James McCartney

import tweepy
import config
import json
import os


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
            returnTweets[tweet.id] = tweet.text


    if CheckFor200:
        while len(returnTweets) <= 200:
            lastID = tweets[-1].id
            print(lastID)
            tweets = api.user_timeline(screen_name=Username, count=200, start_id=lastID)
            for tweet in tweets:
                if not tweet.text.startswith("RT"):
                    print(re.sub(r'^https?:\/\/.*[\r\n]*', '', tweet.text, flags=re.MULTILINE))
                    returnTweets[tweet.id] = re.sub(r'^https?:\/\/.*[\r\n]*', '', tweet.text, flags=re.MULTILINE)
                    #re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
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

def markovAndTweet(Username):
    '''
    Prepares markov tuples and passes to markov chain method
    '''
    # TODO: Pass to Lucy's markov chain
    return saveMarkovTuples(Username,saveTweets(Username))


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

#tweets = grabUserTweets('JimJam707',False)
markovAndTweet('realDonaldTrump')
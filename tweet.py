import tweepy, sys
import configparser

TWEET_LENGTH = 140

tweepy.

def tweetString(tweet):
    """Takes a string and tweets it"""
    if len(tweet) > TWEET_LENGTH:
        print("Tweet length greater than", TWEET_LENGTH)
    elif len(tweet) == 0:
        print("Tweet length is 0")
    else:
        print("Tweeting:", tweet)
        try:
            api.update_status(tweet)
        except:
            print("Tweet failed")


print(readConfig())

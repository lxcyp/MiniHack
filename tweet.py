import tweepy, sys
import configparser

TWEET_LENGTH = 140

def readConfig():
    path = sys.path[0]
    config = configparser.ConfigParser()
    config.read(path + '/test.cfg')

    bot_username = config.get('TWITTER', 'bot_username')
    api_key = config.get('TWITTER', 'api_key')
    api_secret = config.get('TWITTER', 'api_secret')
    return bot_username, api_key, api_secret

def tweetString(tweet):
    """Takes a string and tweets it"""
    if len(tweet) > TWEET_LENGTH:
        print("Tweet length greater than", TWEET_LENGTH)
    elif len(tweet) == 0:
        print("Tweet length is 0")
    else:
        print("Tweeting:", tweet)
        try:
            print("tweet")
        except:
            print("Tweet failed")


print(readConfig())
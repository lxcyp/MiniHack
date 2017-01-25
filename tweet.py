import Twitter, tweepy

TWEET_LENGTH = 140
LOG_FILE = "past tweets.txt"

auth = Twitter.getAuth()

def tweetString(tweet):
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
        except:
            print("Tweet failed")

def logTweet(tweet):
    file = open(LOG_FILE, 'a')
    file.write(tweet + "\n")
    file.close()
    

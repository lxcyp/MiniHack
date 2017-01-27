import random
import json
import configparser
import tweet
import random

def buildChain(markov_array, starting_length):
    TWEET_MAX = 140 - starting_length
    current_tweet = ""
    finished_tweet = False
    first_tuple = random.choice(markov_array)
    current_tweet += first_tuple[0]
    next_word = first_tuple[1]
    start_word = next_word

    while not finished_tweet:
        finished_tweet = True
        next_word = findWord(start_word, markov_array)
        if len(current_tweet)+len(next_word)+1 < 140:
            finished_tweet = False
            current_tweet = current_tweet + " " + next_word
            start_word = next_word

    tweet.tweetString(current_tweet)

def findWord(last_word, markov_array):
    candidate_words = []
    for i in markov_array:
        if i[0] == last_word:
            candidate_words.append(i[1])
        
    if len(candidate_words) == 0:
        return " "
    else:
        return random.choice(candidate_words)

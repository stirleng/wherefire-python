import csv
import tweepy
from textwrap import wrap
#api_secrets.py
import api_secrets

#constants
#=========

MAX_TWEET_LENGTH = 280

#\constants
#==========

def tweet(new_incidents_fire_names_list):
    # creates the tweepy Client object
    client = tweepy.Client(consumer_key=api_secrets.consumer_key, consumer_secret=api_secrets.consumer_secret, access_token=api_secrets.access_token, access_token_secret=api_secrets.access_token_secret) 

    text_needed = "The new fires are: " + ", ".join(new_incidents_fire_names_list)

    tweet_text_list = wrap(text_needed, MAX_TWEET_LENGTH)

    # tweets the fire names
    for tweet_text in tweet_text_list:
        client.create_tweet(text=tweet_text)


#TODO:: remove testing code below
if __name__ == "__main__":
    #tweet(insert_list_here)
    pass
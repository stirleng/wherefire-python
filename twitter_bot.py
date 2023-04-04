import tweepy
#api_secrets.py
import api_secrets

#constants
#=========

MAX_TWEET_LENGTH = 280

#\constants
#==========

def tweet(tweet_text_list):
    # creates the tweepy Client object
    client = tweepy.Client(consumer_key=api_secrets.consumer_key, consumer_secret=api_secrets.consumer_secret, access_token=api_secrets.access_token, access_token_secret=api_secrets.access_token_secret) 
    
    # tweets the fire names
    for tweet_text in tweet_text_list:  #need tweet list since may be multiple new fires between checks
        client.create_tweet(text=tweet_text)


#TODO:: remove testing code below
if __name__ == "__main__":
    #tweet(insert_list_here)
    pass
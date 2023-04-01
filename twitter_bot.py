import csv
import tweepy
#api_secrets.py
import api_secrets

#constants
#=========

MAX_TWEET_LENGTH = 280

#\constants
#==========

def tweet(new_fire_names):
    # creates the tweepy Client object
    client = tweepy.Client(consumer_key=api_secrets.consumer_key, consumer_secret=api_secrets.consumer_secret, access_token=api_secrets.access_token, access_token_secret=api_secrets.access_token_secret) 

    tweet_text_list = []

    with open("fire_data.csv", "r") as fire_data_file:
        reader = csv.reader(fire_data_file)
        for new_fire_name in new_fire_names:
            for row in reader:  #slow (O(n^2)), possibly worth optimizing
                if any(row) and new_fire_name == row[0]: #any(row) checks to make sure the row is not empty
                    county_name = row[1]
                    date_started = row[2]
                    tweet_text = "ALERT\n\nNew fire: " + new_fire_name + "\nCounty: " + county_name + "\nStarted on: " + date_started + "\n"
                    tweet_text_list.append(tweet_text)
        
    print("new_fire_names: ",new_fire_names)
    print("tweets: ",tweet_text_list)
    # tweets the fire names
    for tweet_text in tweet_text_list:  #need tweet list since may be multiple new fires between checks
        client.create_tweet(text=tweet_text)


#TODO:: remove testing code below
if __name__ == "__main__":
    #tweet(insert_list_here)
    pass
#webscraper is webscraper.py
import webscraper
#twitter_bot is twitter_bot.py
import twitter_bot
import time
import pandas as pd

#constants
#=========

HOUR_IN_SECONDS = 86400
CSV_COLUMN_NAMES = ['name','county','date_started','latitude','longitude']

#\constants
#==========

def main():
        blank_dict = {key: [] for key in CSV_COLUMN_NAMES}
        new_fire_df = pd.DataFrame.from_dict(blank_dict)
        new_fire_df.to_csv('fire_data.csv', header=CSV_COLUMN_NAMES, index=False)
    #main server loop
    #while(1):
        #wait an hour between webscraping checks
        #time.sleep(HOUR_IN_SECONDS)
        new_incidents_available, new_fire_names = webscraper.update_data_file()
        if new_incidents_available == True:
            twitter_bot.tweet(compile_tweet_text(new_fire_names))

def compile_tweet_text(new_fire_names):
    tweet_text_list = []
    df = pd.read_csv('fire_data.csv')
    search_column_name = CSV_COLUMN_NAMES[0]
    for new_fire_name in new_fire_names:
        fire_result = df[df[search_column_name] == new_fire_name]
        county_name = fire_result[CSV_COLUMN_NAMES[1]][0]
        date_started = fire_result[CSV_COLUMN_NAMES[2]][0]
        latitude = fire_result[CSV_COLUMN_NAMES[3]][0]
        longitude = fire_result[CSV_COLUMN_NAMES[4]][0]
        tweet_text = "ALERT\n\nNew fire: " + new_fire_name + "\nCounty: " + county_name + "\nStarted on: " + date_started + "\n"
        tweet_text_list.append(tweet_text)
    return tweet_text_list

if __name__ == "__main__":
    main()
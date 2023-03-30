#webscraper is webscraper.py
import webscraper
import time

#constants
#=========

HOUR_IN_SECONDS = 86400

#\constants
#==========

def main():
    #main server loop
    while(1):
        #wait an hour between webscraping checks
        time.sleep(HOUR_IN_SECONDS)

        new_incidents_available, new_incidents_fire_names_list = webscraper.update_data_file()
        if new_incidents_available == True:
            twitter_bot.tweet(new_incidents_fire_names_list)


if __name__ == "__main__":
    main()
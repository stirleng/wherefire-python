#webscraper is webscraper.py
import webscraper
#twitter_bot is twitter_bot.py
import twitter_bot
import time
import pandas as pd
#import geopandas as gpd
#from shapely.geometry import Point, Polygon

#globals
#=======

gdf_list = [] #a list of all geodataframes

#=======
#globals

#constants
#=========

HOUR_IN_SECONDS = 3600
CSV_COLUMN_NAMES = ['name','county','date_started','latitude','longitude']
SHAPEFILE_NAMES = ['./shapefiles/full_california_fhsz/fhszs06_3.shp']

#\constants
#==========


def main():
        #read_shapefiles()
        #blank_dict = {key: [] for key in CSV_COLUMN_NAMES}
        #new_fire_df = pd.DataFrame.from_dict(blank_dict)
        #new_fire_df.to_csv('fire_data.csv', header=CSV_COLUMN_NAMES, index=False)
    #main server loop
    #while(1):
        #wait an hour between webscraping checks
        #time.sleep(HOUR_IN_SECONDS)
    new_fire_names = webscraper.update_data_file()
    if new_fire_names:  #if the list of new fires is not empty
            twitter_bot.tweet(compile_tweet_text(new_fire_names))

def compile_tweet_text(new_fire_names):
    tweet_text_list = []
    df = pd.read_csv('/home/stirleng/Documents/wherefire-python/fire_data.csv')
    #print(df)
    search_column_name = CSV_COLUMN_NAMES[0]
    for new_fire_name in new_fire_names:
        fire_result = df[df[search_column_name] == new_fire_name]
        print(new_fire_name)
        county_name = fire_result.loc[:,CSV_COLUMN_NAMES[1]].tolist()[0]
        date_started = fire_result.loc[:,CSV_COLUMN_NAMES[2]].tolist()[0]
        latitude = fire_result.loc[:,CSV_COLUMN_NAMES[3]].tolist()[0]
        longitude = fire_result.loc[:,CSV_COLUMN_NAMES[4]].tolist()[0]
        #fhsz_text = ""
        #if fhsz(latitude, longitude):
        #    fhsz_text = "The fire is in an area designated as a fire hazard zone.\n"
        tweet_text = "New wildfire in California - " + new_fire_name + "\nCounty: " + county_name + "\nStart Date: " + date_started + "\n" #+ fhsz_text
        tweet_text_list.append(tweet_text)
    return tweet_text_list

#constructs fhsz polygons from shapefiles
#def read_shapefiles():
#    for shapefile_name in SHAPEFILE_NAMES:
#        gdf = gpd.read_file(shapefile_name) #gdf is geodataframe
#        gdf_list.append(gdf)        

#returns what classification of fire hazard severity zone a location is in (none,)
#def fhsz(lat,long):
#   point = Point(lat,long)
#   for gdf in gdf_list:
#       for polygon in gdf.geometry:
#           if point.within(polygon):
#               print('in fhsz')

if __name__ == "__main__":
    main()

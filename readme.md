https://twitter.com/wherefire2

Run on a Raspberry Pi Zero W.

# Setup - Windows
Install python3. Then install pip, then using pip, install requests, pandas, geopandas, shapely (pyshp), tweepy, Beautiful Soup, and the lxml parser.

# Overview
Wrote a webscraper in Python using Beautiful Soup to get wildfire data from public records and store it using Pandas in a small database.
Wrote code to access the Twitter API in order to authenticate and compose tweets.
Set up a Cron job on a Raspberry Pi Zero W to run all components.

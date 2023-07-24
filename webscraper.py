import requests
import pandas as pd
from bs4 import BeautifulSoup as BS
import threading

#constants
#=========

#tbody tag only occurs once on page (tbody is short for table body)
RESULT_TABLE_TAG = 'tbody'

#link tags (link to specific fire incident page)
FIRE_NAMES_TAG = 'th'

#specify certain request headers so the website doesn't 403 our request and we receive an xml response
headers = {  'Connection': 'close', 'Accept': 'application/xml', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'} 

#other constants
CURRENT_YEAR_URL = 'https://www.fire.ca.gov/incidents/2023/'
TEST_YEAR_URL = 'https://www.fire.ca.gov/incidents/2022/'
INCIDENT_URL_BASE = CURRENT_YEAR_URL
LAT_LONG_TEXT = 'Latitude / Longitude'
CSV_COLUMN_NAMES = ['name','county','date_started','latitude','longitude']

#/constants
#==========

def update_data_file():
    #get webpage xml from response
    with requests.Session() as s:
        response = s.get(CURRENT_YEAR_URL, headers=headers)
        response_xml = response.text
    #parse xml using lxml parser
    soup = BS(response_xml, 'lxml')

    #find data table in page
    data_table = soup.find(RESULT_TABLE_TAG)

    #find all fire name elements (hypertext)
    fire_name_elements = data_table.find_all(FIRE_NAMES_TAG)

    #create lists for each fire attribute
    fire_names = []
    fire_counties = []
    fire_start_dates = []
    fire_latitudes = []
    fire_longitudes = []
    incident_urls = []
    #iterate through table elements and store text
    for fire_name_element in fire_name_elements:
        fire_name_text = fire_name_element.contents[1].text.strip()
        print(fire_name_text)
        fire_county_name_element = fire_name_element.next_sibling.next_sibling #idk why it needs an extra .next_sibling but it does
        fire_date_started_element = fire_county_name_element.next_sibling.next_sibling
        fire_names.append(fire_name_text) #.child because fire names have an extra parent wrapper
        fire_counties.append(fire_county_name_element.text.strip())
        fire_start_dates.append(fire_date_started_element.text.strip())
        split_date = fire_date_started_element.text.split('/')
        #TODO:: use a regex to remove all alphanumeric characters in the fire name (to use in url - maybe only replace chars not permitted in urls?)
        stripped_date = split_date[0].lstrip('0') + "/" + split_date[1].lstrip('0') + "/" + fire_name_text.replace("(","").replace(")","").replace(" ", "-")
        incident_url = INCIDENT_URL_BASE + stripped_date
        incident_urls.append(incident_url)
        #TODO:: use forking to make the following faster
        with requests.Session() as s:
            response = s.get(incident_url, headers=headers)
            response_xml = response.text
            soup = BS(response_xml, 'lxml')
            lat_long_title_element = soup.find(text=LAT_LONG_TEXT)
            lat_long_element = lat_long_title_element.parent.next_sibling.next_sibling
            #isolate latitude and longitude and convert from string to float
            lat_long = lat_long_element.text.replace("[", "").replace("]", "").replace(" ", "").split(",")
            for val in lat_long:
                float(val)
            fire_latitudes.append(lat_long[0])
            fire_longitudes.append(lat_long[1])


    #find which fires are new
    new_incidents_available = False
    new_incidents_fire_names = []
    df = pd.read_csv('fire_data.csv')
    search_column_name = CSV_COLUMN_NAMES[0]
    new_fire_data = {key: [] for key in CSV_COLUMN_NAMES} #create a dict of new data to append to csv
    for fire_name, county_name, date_started,latitude,longitude in zip(fire_names, fire_counties, fire_start_dates,fire_latitudes,fire_longitudes):
        new_fire = df[df[search_column_name] == fire_name]
        if new_fire.empty:
            new_incidents_available = True
            new_incidents_fire_names.append(fire_name)
            new_fire_data[CSV_COLUMN_NAMES[0]].append(fire_name)
            new_fire_data[CSV_COLUMN_NAMES[1]].append(county_name)
            new_fire_data[CSV_COLUMN_NAMES[2]].append(date_started)
            new_fire_data[CSV_COLUMN_NAMES[3]].append(latitude)
            new_fire_data[CSV_COLUMN_NAMES[4]].append(longitude)
    new_fire_df = pd.DataFrame.from_dict(new_fire_data)
    new_fire_df.to_csv('fire_data.csv', mode='a', header=False, index=False)

    #note: returns a tuple of two vars
    return new_incidents_available, new_incidents_fire_names
                

#TODO:: remove testing code below
if __name__ == "__main__":
    update_data_file()
    pass
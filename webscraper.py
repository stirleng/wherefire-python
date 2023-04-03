import requests
import csv
from bs4 import BeautifulSoup as BS

#constants
#=========

#tbody tag only occurs once on page (tbody is short for table body)
RESULT_TABLE_TAG = "tbody" 

#link tags (link to specific fire incident page)
FIRE_NAMES_TAG = "th"

CURRENT_YEAR_URL = 'https://www.fire.ca.gov/incidents'
PREV_YEAR_URL = 'https://www.fire.ca.gov/incidents/2022/'
INCIDENT_URL_BASE = PREV_YEAR_URL #TODO:: change to CURRENT_YEAR_URL when done testing
LAT_LONG_TEXT = 'Latitude / Longitude'

#specify certain request headers so the website doesn't 403 our request and we receive an xml response
headers = {  'Connection': 'close', 'Accept': 'application/xml', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'} 

#/constants
#==========

def update_data_file():
    #get webpage xml from response
    with requests.Session() as s:
        response = s.get(PREV_YEAR_URL, headers=headers)
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
    fire_locations = []
    #iterate through table elements and store text
    for fire_name_element in fire_name_elements:
        fire_name_text = fire_name_element.contents[1].text.strip()
        fire_county_name_element = fire_name_element.next_sibling.next_sibling #idk why it needs an extra .next_sibling but it does
        fire_date_started_element = fire_county_name_element.next_sibling.next_sibling
        fire_names.append(fire_name_text) #.child because fire names have an extra parent wrapper
        fire_counties.append(fire_county_name_element.text.strip())
        fire_start_dates.append(fire_date_started_element.text.strip())
        split_date = fire_date_started_element.text.split('/')
        #TODO:: use a regex to remove all alphanumeric characters in the fire name (to use in url - maybe only replace chars not permitted in urls?)
        stripped_date = split_date[0].lstrip('0') + "/" + split_date[1].lstrip('0') + "/" + fire_name_text.replace("(","").replace(")","").replace(" ", "-")
        incident_url = INCIDENT_URL_BASE + stripped_date
        with requests.Session() as s:
            response = s.get(incident_url, headers=headers)
            response_xml = response.text
            soup = BS(response_xml, 'lxml')
            lat_long_title_element = soup.find(string=LAT_LONG_TEXT)
            print(fire_name_text)
            lat_long_element = lat_long_title_element.parent.next_sibling.next_sibling
            lat_long = lat_long_element.text.replace("[", "").replace("]", "").replace(" ", "")
            fire_locations.append(lat_long)


    #find which fires are new
    new_incidents_available = False
    new_incidents_fire_names = []
    #TODO:: possibly remove newline='' for raspberry pi since it probably uses lf not crlf
    with open("fire_data.csv", "r+", newline='') as fire_data_file: #(r+ signifies both reading and writing) (newline='' prevents it from writing 2 newlines on Windows)
        writer = csv.writer(fire_data_file)
        contents = fire_data_file.read()
        for fire_name, county_name, date_started,location in zip(fire_names, fire_counties, fire_start_dates,fire_locations):
            if fire_name not in contents:
                new_incidents_available = True
                new_incidents_fire_names.append(fire_name)
                writer.writerow([fire_name,county_name,date_started,location])
            #TODO:: remove testing code below
            # print(fire_name.string)

    #note: returns a tuple of two vars
    return new_incidents_available, new_incidents_fire_names
                

#TODO:: remove testing code below
if __name__ == "__main__":
    update_data_file()
    pass
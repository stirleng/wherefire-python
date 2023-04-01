import requests
import csv
from bs4 import BeautifulSoup as BS

#constants
#=========

#tbody tag only occurs once on page (tbody is short for table body)
RESULT_TABLE_TAG = "tbody" 

#link tags (link to specific fire incident page)
FIRE_NAMES_TAG = "th"

current_year_url = 'https://www.fire.ca.gov/incidents'
prev_year_url = 'https://www.fire.ca.gov/incidents/2022/'

#specify certain request headers so the website doesn't 403 our request and we receive an xml response
headers = {  'Connection': 'close', 'Accept': 'application/xml', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'} 

#/constants
#==========

def update_data_file():
    #get webpage xml from response
    with requests.Session() as s:
        response = s.get(prev_year_url, headers=headers)
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
    #iterate through table elements and store text
    for fire_name_element in fire_name_elements:
        fire_county_name_element = fire_name_element.next_sibling.next_sibling #idk why it needs an extra .next_sibling but it does
        fire_date_started_element = fire_county_name_element.next_sibling.next_sibling
        fire_names.append(fire_name_element.contents[1].text.strip()) #.child because fire names have an extra parent wrapper
        fire_counties.append(fire_county_name_element.text.strip())
        fire_start_dates.append(fire_date_started_element.text.strip())

    #find which fires are new
    new_incidents_available = False
    new_incidents_fire_names = []
    new_incidents_fire_counties = []
    new_incidents_dates_started = []
    #TODO:: possibly remove newline='' for raspberry pi since it probably uses lf not crlf
    with open("fire_data.csv", "r+", newline='') as fire_data_file: #(r+ signifies both reading and writing) (newline='' prevents it from writing 2 newlines on Windows)
        writer = csv.writer(fire_data_file)
        contents = fire_data_file.read()
        for fire_name, county_name, date_started in zip(fire_names, fire_counties, fire_start_dates):
            if fire_name not in contents:
                new_incidents_available = True
                new_incidents_fire_names.append(fire_name)
                new_incidents_fire_counties.append(county_name)
                new_incidents_dates_started.append(date_started)
                writer.writerow([fire_name,county_name,date_started])
            #TODO:: remove testing code below
            # print(fire_name.string)

    #note: returns a tuple of two vars
    return new_incidents_available, new_incidents_fire_names
                

#TODO:: remove testing code below
if __name__ == "__main__":
    update_data_file()
    pass
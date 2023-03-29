import requests
import csv
from bs4 import BeautifulSoup as BS

#constants
#=========

#tbody tag only occurs once on page (tbody is short for table body)
RESULT_TABLE_TAG = "tbody" 

#link tags (link to specific fire incident page)
FIRE_NAMES_TAG = "a"

current_year_url = 'https://www.fire.ca.gov/incidents'
prev_year_url = 'https://www.fire.ca.gov/incidents/2022/'

#specify certain request headers so the website doesn't 403 our request and we receive an xml response
headers = {'Accept': 'application/xml', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'} 

#/constants
#==========

def update_data_file():
    #get webpage xml from response
    response_xml = requests.get(prev_year_url, headers=headers)
    response_text = response_xml.text

    #parse xml using lxml parser
    soup = BS(response_text, 'lxml')

    data_table = soup.find(RESULT_TABLE_TAG)
    fire_names = data_table.find_all(FIRE_NAMES_TAG)
    for fire_name in fire_names:
        print(fire_name.string)

if __name__ == "__main__":
    #update_data_file()
    pass
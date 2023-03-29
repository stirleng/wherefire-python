import requests
from bs4 import BeautifulSoup as BS

#constants
RESULT_TABLE_TAG = "tbody" #short for table body
FIRE_NAMES_TAG = "a" #includes a link to the specific fire page
current_url = 'https://www.fire.ca.gov/incidents'
prev_year_url = 'https://www.fire.ca.gov/incidents/2022/'
headers = {'Accept': 'application/xml', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'}



def main():
    response_xml = requests.get(prev_year_url, headers=headers)
    response_text = response_xml.text

    soup = BS(response_text, 'lxml')
    data_table = soup.find(RESULT_TABLE_TAG)
    fire_names = data_table.find_all(FIRE_NAMES_TAG)
    for fire_name in fire_names:
        print(fire_name.string)

if __name__ == "__main__":
    main()
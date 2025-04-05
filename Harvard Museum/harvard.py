import os
import json
import requests
from bs4 import BeautifulSoup
import regex as re

def get_api_key(filename):
    '''Input: filename where the API key is stored
    
    Output: api_key as a string
    '''
    # source_dir = os.path.dirname(__file__)
    # full_path = os.path.join(source_dir, filename)
    # with open(full_path) as f:
    with open(filename) as f:
        return f.read()

def call_api(harvard_api_key):
    r = requests.get('https://api.harvardartmuseums.org/object',
        params = {
            'apikey': harvard_api_key,
            'page' : 2,
            'fields': 'accessionyear,objectnumber,id'
        })
    #print(r.status_code, r.json())

    json_data = r.json()

    with open("harvard.json", 'w') as outfile:
        json.dump(json_data, outfile, indent = 4)

    print(type(json_data))
    print(json_data['info']['pages'])

    for record in json_data["records"]:
        print(record['id'])


##verification level
##artist gender --> person id --> person API --> gender


def find_harvard_directors():
    url = 'https://en.wikipedia.org/wiki/Harvard_Art_Museums'
    resp = requests.get(url)
    if resp.status_code == 200:

        soup = BeautifulSoup(resp.content, 'html.parser')
        directors_list = []

        page_content = soup.find('div', id = "mw-content-text", class_= "mw-body-content")
        d_list = page_content.find('ul')
        directors_data = d_list.find_all('li')
        for d in directors_data:
            #print(d.text)
            name_pattern = r'^(.+):'
            start_year_pattern = r': (\d{4})'
            end_year_pattern = r'(?:–\d{4}|–[a-z]+)'

            name = re.findall(name_pattern, d.text)[0]
            start_year = re.findall(start_year_pattern, d.text)[0]
            end_year = re.findall(end_year_pattern, d.text)[0].strip("–")

            director_dict = {'name': name, 'start_year': start_year, 'end_year': end_year}
            directors_list.append(director_dict)
        return directors_list
    return None



def main():
    #harvard_api_key = get_harvard_api_key()
    #call_api(harvard_api_key)
    print(find_harvard_directors())

if __name__ == "__main__":
    main()

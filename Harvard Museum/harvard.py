import os
import json
import requests
from bs4 import BeautifulSoup
import regex as re

def get_harvard_api_key(filename):
    '''Input: filename where the API key is stored
    
    Output: api_key as a string
    '''
    # source_dir = os.path.dirname(__file__)
    # full_path = os.path.join(source_dir, filename)
    # with open(full_path) as f:
    with open(filename) as f:
        return f.read()
    
# def set_up_art_database():
#     pass

# def create_pieces_of_art_table(cur, conn):
#     pass

def get_art_data(harvard_api_key):
    art_list = []
    request = requests.get('https://api.harvardartmuseums.org/object',
        params = {
            'apikey': harvard_api_key,
            'page' : 1,
            'fields': 'accessionyear,objectnumber,people,id'
        })
    json_data = request.json()
    num_of_pages = json_data['info']['pages']
    # for page_num in range(1, num_of_pages+1):
    for page_num in range(1,5):
        r = requests.get('https://api.harvardartmuseums.org/object',
        params = {
            'apikey': harvard_api_key,
            'page' : page_num,
            'fields': 'accessionyear,people,id'
        })
        page_data = r.json()
        print(page_data)
        for d in page_data['records']:
            art_dict = {}
            id = d['id']
            accessionyear = d['accessionyear']
            #only adding the art to the dictionary if the accession year is not None
            if accessionyear:
                people = d.get('people')
                female = False
                if people:
                    for p in people:
                        if p['gender'] == 'female':
                            female = True
                art_dict['id'] = id
                art_dict['accessionyear'] = accessionyear
                art_dict['gender'] = female
                art_list.append(art_dict)
    print(art_list)
    return art_list

    # for record in json_data["records"]:
    #     print(record['id'])
    

##GO THROUGH EACH PAGE AND GET ALL THE OBJECT DATA AND THE ARTIST GENDER 
## AND THEN ADD TO JSON file

def write_data_to_file(json_data, filename):
    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile, indent = 4)


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
    harvard_api_key = get_harvard_api_key("Harvard_API_KEY.txt")
    data = get_art_data(harvard_api_key)
    write_data_to_file(data, "harvard.json")
    directors = find_harvard_directors()
    write_data_to_file(directors, "harvard_directors.json")
    



if __name__ == "__main__":
    main()

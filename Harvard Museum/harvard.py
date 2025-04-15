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

##This function did not add meaningful data to the database
# def get_verification_level(art_id, harvard_api_key):
#     request = requests.get(f'https://api.harvardartmuseums.org/object/{art_id}',
#         params = {
#             'apikey': harvard_api_key,
#             'fields': 'verificationlevel'
#         })
#     json_data = request.json()
#     return json_data.get('verificationlevel')

def get_art_data(harvard_api_key):
    art_list = []
    #finding the total number of pages to determine how many times to call the API to get all the data
    request = requests.get('https://api.harvardartmuseums.org/object',
        params = {
            'apikey': harvard_api_key,
            'page' : 1,
            'fields': 'accessionyear,objectnumber,people,id'
        })
    json_data = request.json()
    num_of_pages = json_data['info']['pages']

    ##GO THROUGH EACH PAGE AND GET ALL THE OBJECT DATA AND THE ARTIST GENDER 
    # for page_num in range(1, num_of_pages+1): #loop through each possible page
    for page_num in range(1,num_of_pages+1,200): # artificially choosing the number of pages retrieved to get less than 1,000 pieces of art rather than the whole catalog of ~25,000
        r = requests.get('https://api.harvardartmuseums.org/object',
        params = {
            'apikey': harvard_api_key,
            'page' : page_num,
            'fields': 'accessionyear,people,id'
        })
        page_data = r.json()
        #print(page_data)
        for d in page_data['records']:
            art_dict = {}
            id = d['id']
            #verificationlevel = get_verification_level(id, harvard_api_key)
            accessionyear = d['accessionyear']
            #only adding the art to the dictionary if the accession year is not None
            if accessionyear:
                people = d.get('people')
                gender = 'Male/Unknown'
                if people:
                    for p in people:
                        if p['gender'] == 'female':
                            gender = 'Female'
                art_dict['id'] = id
                #art_dict['verificationlevel'] = verificationlevel
                art_dict['accessionyear'] = accessionyear
                art_dict['gender'] = gender
                art_list.append(art_dict)
    #print(art_list)
    return art_list

def write_data_to_file(json_data, filename):
    '''Input:

    '''
    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile, indent = 4)


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

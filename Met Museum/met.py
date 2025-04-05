import requests
import json

def calling_api():
    base_url = 'https://collectionapi.metmuseum.org/public/collection/v1/search?'
    # url = 'https://collectionapi.metmuseum.org/public/collection/v1/search?isOnView=True&artistGender=female&country=France&q=flower'

    params = {

    'q': '',
    # 'isOnView': True,
    'artistGender': 'female',
    'country': 'United States'

    }

    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        print(type(response.text))
        data = response.json()
        # print(data)
        print(type(data))

    return data

def create_file_from_json_data(filename, data):

    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent = 4)
    



data = calling_api()
create_file_from_json_data('outfile', data)

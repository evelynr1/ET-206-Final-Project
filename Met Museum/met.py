import requests
import json


def get_objectIDs():
    ''' 
    Gets a list of objectIDs from the Met Museum API for highlighted objects

    Returns:
        list: objectIDs (integers) representing highlighted artworks
    '''

    base_url = 'https://collectionapi.metmuseum.org/public/collection/v1/search?'
    params = {
        'q': ' ',
        'isHighlight': 'true'
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    # print(len(data['objectIDs']))
    return data.get("objectIDs", [])  

def get_object_details(objectIDs):
    '''
    Gets details for each objectID, filtering by accession year (must be greater than or equal to 1879) 
    + handling missing artist gender cases

    Args:
        objectIDs (list): a list of object IDs to retrieve details for

    Returns:
        list: a list of dictionaries containing objectID, artistGender, and accessionYear
    '''
    base_url = f'https://collectionapi.metmuseum.org/public/collection/v1/objects/'
    result = []
    for objectID in objectIDs:
        response = requests.get(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{objectID}')
        if response.status_code == 200:
            art = response.json()

            try:
                year = int(art.get("accessionYear", 0))
                if year >= 1879:
                    gender = art.get("artistGender", '')
                    if gender == '':
                        gender = 'Male/Unknown'
                    data = {
                        "objectID": art.get("objectID"),
                        "artistGender": gender,
                        "accessionYear": year
                    }
                    result.append(data)
            except:
                pass
    return result

def create_file_from_json_data(filename, data):
    '''
    Saves data to a JSON file

    Args:
        filename (str):  name of the file to save data to
        data (dict): data to write to the JSON file
    '''

    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent = 4)


def main():
    '''
    Fetches object IDs, gets their details,
    and saves results to a JSON file
    '''
    objectIDs = get_objectIDs()
    details = get_object_details(objectIDs)
    create_file_from_json_data('met.json', details)

if __name__ == "__main__":
    main()

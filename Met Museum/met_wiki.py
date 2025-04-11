from bs4 import BeautifulSoup
import re
import os
import requests
import json



def load_wiki_results():

    url = 'https://en.wikipedia.org/wiki/List_of_directors_of_the_Metropolitan_Museum_of_Art'

    response = requests.get(url)
    result = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="wikitable") # getting main table
        # print(table.text)
        row_tags = table.find_all("tr") # getting table rows
        for tag in row_tags:
            director_dict = {}
            data_tags = tag.find_all("td") # getting data from each row
            if data_tags:
                director_name = data_tags[2].text.strip()
                director_dict["name"] = director_name
                tenure = data_tags[3].text.split()
                # print(tenure)
                if len(tenure) > 1:
                    start_year = tenure[0]
                    end_year = tenure[2]
                    director_dict["start_year"] = start_year
                    director_dict["end_year"] = end_year
                else:
                    start_year = tenure[0]
                    end_year = None
                    director_dict["start_year"] = start_year
                    director_dict["end_year"] = end_year

                result.append(director_dict)

    return result

data = load_wiki_results()

def create_file_from_json_data(filename, data):

    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent = 4)

create_file_from_json_data('met_directors.json', data)


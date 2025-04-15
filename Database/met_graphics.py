import matplotlib.pyplot as plt
import sqlite3
import os

def get_data(con, cur):
    '''
    Gets and sorts artwork acquisition data (stored in database) by museum director and artist gender

    Parameters:
        con: connection object to SQLite database
        cur: cursor object used to execute SQL queries

    Returns:
        dict: dictionary where each key is a director's name and the value is another
              dictionary with keys 'Male Artists' and 'Female Artists' and their counts
    '''
    director_dict = {}
    director_names = cur.execute('''SELECT name 
    FROM MetDirectors''').fetchall()

    directors_male_art = cur.execute('''SELECT MetDirectors.name, COUNT(*) 
                        FROM MetDirectors
                        JOIN MetArt
                        ON MetArt.accessionYear BETWEEN MetDirectors.start_year AND MetDirectors.end_year
                        WHERE MetArt.artistGender = 2
                        GROUP BY MetDirectors.name, MetArt.artistGender;
                        ''').fetchall()

    directors_female_art = cur.execute('''SELECT MetDirectors.name, COUNT(*) 
                        FROM MetDirectors
                        JOIN MetArt
                        ON MetArt.accessionYear BETWEEN MetDirectors.start_year AND MetDirectors.end_year
                        WHERE MetArt.artistGender = 1
                        GROUP BY MetDirectors.name, MetArt.artistGender;
                        ''').fetchall()

    for name_tuple in director_names:
        name = name_tuple[0]
        director_dict[name] = {"Male Artists": 0, "Female Artists": 0}

    for name, count in directors_male_art:
        director_dict[name]["Male Artists"] = count

    for name, count in directors_female_art:
        director_dict[name]["Female Artists"] = count

    return director_dict
    
def get_harvard_data(conn, cur):
    '''
    Gets and sorts artwork acquisition data (stored in database) by museum director and artist gender
    (functionally same as get_data() above, just using Harvard tables)

    Parameters:
        con: connection object to SQLite database
        cur: cursor object used to execute SQL queries

    Returns:
        dict: dictionary where each key is a director's name and the value is another
              dictionary with keys 'Male Artists' and 'Female Artists' and their counts
    '''

    director_dict = {}
    director_names = cur.execute('''SELECT name 
    FROM HarvardDirectors''').fetchall()

    directors_male_art = cur.execute('''SELECT HarvardDirectors.name, COUNT(*) 
                        FROM HarvardDirectors
                        JOIN HarvardArt
                        ON HarvardArt.accessionYear BETWEEN HarvardDirectors.start_year AND HarvardDirectors.end_year
                        WHERE HarvardArt.artistGender = 2
                        GROUP BY HarvardDirectors.name, HarvardArt.artistGender;
                        ''').fetchall()

    directors_female_art = cur.execute('''SELECT HarvardDirectors.name, COUNT(*) 
                        FROM HarvardDirectors
                        JOIN HarvardArt
                        ON HarvardArt.accessionYear BETWEEN HarvardDirectors.start_year AND HarvardDirectors.end_year
                        WHERE HarvardArt.artistGender = 1
                        GROUP BY HarvardDirectors.name, HarvardArt.artistGender;
                        ''').fetchall()

    for name_tuple in director_names:
        name = name_tuple[0]
        director_dict[name] = {"Male Artists": 0, "Female Artists": 0}

    for name, count in directors_male_art:
        director_dict[name]["Male Artists"] = count

    for name, count in directors_female_art:
        director_dict[name]["Female Artists"] = count

    return director_dict

def make_total_gender_pie(director_dict):
    total_male = 0
    total_female = 0

    for counts in director_dict.values():
        total_male += counts['Male Artists']
        total_female += counts['Female Artists']

    labels = ['Female Artists', 'Male Artists']
    sizes = [total_female, total_male]
    colors = ['firebrick', 'darkcyan']
    explode = (0.1, 0)  

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Metropolitan Museum Highlights by Artist Gender')
    plt.savefig("met_pie_chart.png")
    plt.show()

def make_comparison_chart(harvard_dict, met_dict):
    '''
    Makes and displays bar chart comparing number of artworks by male and female artists
    between the Harvard and Met museums

    Parameters:
        harvard_dict (dict): dictionary with Harvard director names as keys and counts of male/female artworks as values
        met_dict (dict): dictionary with Met director names as keys and counts of male/female artworks as values

    Chart gets saved as 'comparison_bar_chart.png'
    '''
    met_directors = list(met_dict.keys())
    harvard_directors = list(harvard_dict.keys())

    met_male_count = 0
    met_female_count = 0

    harvard_male_count = 0
    harvard_female_count = 0

    for counts in met_dict.values():
        met_male_count += counts['Male Artists']
        met_female_count += counts['Female Artists']

    for counts in harvard_dict.values():
        harvard_male_count += counts['Male Artists']
        harvard_female_count += counts['Female Artists']

    labels = ['Met Male Artists', 'Met Female Artists', 'Harvard Male Artists', 'Harvard Female Artists']
    values = [met_male_count, met_female_count, harvard_male_count, harvard_female_count]
    colors = ['darkcyan', 'firebrick', 'darkcyan', 'firebrick']

    plt.figure(figsize=(12, 8))
    plt.bar(labels, values, color=colors)
    plt.title('Artworks by Museum and Artist Gender')
    plt.savefig("comparison_bar_chart.png")
    plt.show()

def save_data_to_file(data_dict1, data_dict2, filename):
    '''
    Writes artist gender counts for each director to a txt file

    Parameters:
        data_dict (dict): dictionary of directors with counts of artworks by gender
        filename (str): name of txt file to write the data to
    '''
    with open(filename, 'w') as f:
        f.write(f"Met Director Calculations\n")
        for director, counts in data_dict1.items():
            f.write(f"{director}\n")
            f.write(f"  Male Artists: {counts['Male Artists']}\n")
            f.write(f"  Female Artists: {counts['Female Artists']}\n")
            f.write("\n")

        f.write(f"Harvard Director Calculations\n")
        for director, counts in data_dict2.items():
            f.write(f"{director}\n")
            f.write(f"  Male Artists: {counts['Male Artists']}\n")
            f.write(f"  Female Artists: {counts['Female Artists']}\n")
            f.write("\n")


def main(): 
    dir = os.path.dirname(__file__)+ os.sep
    conn = sqlite3.connect(dir+'Art.db')
    cur = conn.cursor()

    met_dict = get_data(conn, cur)
    harvard_dict = get_harvard_data(conn, cur)

    make_total_gender_pie(met_dict)
    make_comparison_chart(harvard_dict, met_dict)

    save_data_to_file(met_dict, harvard_dict, 'calculations.txt')

if __name__ == '__main__':
    main()

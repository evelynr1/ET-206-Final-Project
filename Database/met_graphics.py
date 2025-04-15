import matplotlib.pyplot as plt
import sqlite3
import os

def get_data(con, cur):
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

# def make_bar_chart(director_dict):
#     directors = []
#     female_counts = []
#     male_counts = []

#     for director in director_dict:
#         directors.append(director)
#         female_counts.append(director_dict[director]['Female Artists'])
#         male_counts.append(director_dict[director]['Male Artists'])

#     female_positions = []
#     i = 0
#     while i < 11:
#         female_positions.append(i)
#         i += 1

#     male_positions = []
#     j = 0
#     while j < len(female_positions):
#         male_positions.append(female_positions[j] + 0.4)
#         j += 1

#     mid_positions = []
#     k = 0
#     while k < len(female_positions):
#         mid = female_positions[k] + 0.2
#         mid_positions.append(mid)
#         k += 1

#     plt.figure(figsize=(14, 7))
#     plt.bar(female_positions, female_counts, width=0.4, label='Female Artists', color='firebrick')
#     plt.bar(male_positions, male_counts, width=0.4, label='Male Artists', color='darkcyan')

#     plt.xticks(mid_positions, directors, rotation=45, ha='right')
#     plt.ylabel('Number of Artworks')
#     plt.title('Metropolitan Museum Highlights by Museum Director and Artist Gender')
#     plt.legend()
#     plt.show()


def make_comparison_chart(harvard_dict, met_dict):
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

def main(): 
    path = '/Users/tessakipke/SI_206/ET-206-Final-Project/Database'
    db_path = os.path.join(path, 'Art.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    met_dict = get_data(conn, cur)
    harvard_dict = get_harvard_data(conn, cur)

    make_total_gender_pie(met_dict)
    make_bar_chart(met_dict)
    make_comparison_chart(harvard_dict, met_dict)

if __name__ == '__main__':
    main()

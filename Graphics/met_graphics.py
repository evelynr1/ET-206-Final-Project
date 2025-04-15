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
    plt.show()


def main(): 
    path = '/Users/tessakipke/SI_206/ET-206-Final-Project/Database'
    db_path = os.path.join(path, 'Art.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    director_dict = get_data(conn, cur)
    make_total_gender_pie(director_dict)
    make_bar_chart(director_dict)


if __name__ == '__main__':
    main()

import matplotlib.pyplot as plt
import sqlite3
import os

def get_data(con, cur):
    director_dict = {}
    director_names = cur.execute('''SELECT name 
    FROM MetDirectors''').fetchall()
    for item in director_names:
        names.append(item[0])
        names.append(item[0])
    print(names)
    print(len(names))


    directors_all_art = cur.execute('''SELECT MetDirectors.name, COUNT(*) 
                        FROM MetDirectors
                        JOIN MetArt
                        ON MetArt.accessionYear BETWEEN MetDirectors.start_year AND MetDirectors.end_year
                        WHERE MetArt.artistGender IN (1,2)
                        GROUP BY MetDirectors.name, MetArt.artistGender;
                        ''').fetchall()

    for item in directors_all_art:
        director_dict[item[0]]
        names.append(item[0])
        counts.append(item[1])


    labels = names
    sizes = counts
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'cyan']
    explode = (0, 0, 0, 0, 0)
 
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.show()

def main(): 
    path = '/Users/tessakipke/SI_206/ET-206-Final-Project/Database'
    db_path = os.path.join(path, 'Art.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    get_data(conn, cur)

    

if __name__ == '__main__':
    main()

import os
import json
import sqlite3

def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return(conn, cur)

def create_gender_table(conn, cur):
    genders = ['Female', 'Male/Unknown']
    cur.execute('''CREATE TABLE IF NOT EXISTS Gender
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    gender TEXT UNIQUE)'''
    )
    for gender in genders:
        cur.execute('''INSERT OR IGNORE INTO Gender (gender)
        VALUES (?)''',
        (gender,))

    conn.commit()

def create_harvard_directors_table(conn, cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS HarvardDirectors
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT UNIQUE,
        start_year INTEGER,
        end_year INTEGER)'''
        )
    conn.commit()

    

    pass

def add_harvard_directors_from_json(conn, cur, filename):
    pass





def main():
    conn, cur = set_up_database("Art.db")
    create_gender_table(conn, cur)
    create_harvard_directors_table(conn, cur)
    add_harvard_directors_from_json(conn, cur, "harvard_directors.json")


if __name__ == "__main__":
    main()

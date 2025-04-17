import os
import json
import sqlite3

def set_up_database(db_name):
    '''Sets up the database. Returns the connection (conn) and cursor (cur)'''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return(conn, cur)

def create_gender_table(conn, cur):
    '''Creates the Genders table within the database using the input connection (conn) and cursor (cur)'''
    genders = ['Female', 'Male/Unknown']
    cur.execute('''CREATE TABLE IF NOT EXISTS Genders
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    gender TEXT UNIQUE)'''
    )
    for gender in genders:
        cur.execute('''INSERT OR IGNORE INTO Genders (gender)
        VALUES (?)''',
        (gender,))

    conn.commit()

def create_harvard_directors_table(conn, cur):
    '''Creates the HarvardDirectors table within the database using the input connection (conn) and cursor (cur)'''
    cur.execute('''CREATE TABLE IF NOT EXISTS HarvardDirectors
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT UNIQUE,
        start_year INTEGER,
        end_year INTEGER)'''
        )
    conn.commit()

def add_harvard_directors_from_json(conn, cur, filename):
    with open(filename, 'r') as file:
        content = json.load(file)

    for item in content:
        cur.execute('''INSERT OR IGNORE INTO HarvardDirectors (name,start_year,end_year) VALUES (?,?,?)''', 
        (item['name'], item['start_year'], item['end_year']))

    conn.commit()

def create_harvard_art_table(conn, cur):
    '''Creates the HarvardArt table within the database using the input connection (conn) and cursor (cur)'''
    cur.execute('''CREATE TABLE IF NOT EXISTS HarvardArt
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        objectID INTEGER UNIQUE,
        accessionYear INTEGER,
        artistGender INTEGER)
        ''')
    conn.commit()

def add_harvard_art_from_json(conn, cur, filename):
    with open(filename, 'r') as f:
        art = json.load(f)

    cur.execute('''SELECT COUNT(*) FROM HarvardArt''')
    num_of_art = cur.fetchone()[0]

    new_inserts = 0
    for piece in art:
        
        if num_of_art < 100:
            if new_inserts >= 25:
                break
        gender = piece['gender']
        gender_id = cur.execute(f'''SELECT id FROM Genders 
        WHERE gender=?''', (f"{gender}",)).fetchone()[0]

        cur.execute('''INSERT OR IGNORE INTO HarvardArt 
                    (objectID,
                    artistGender,
                    accessionYear) 
                    VALUES (?,?,?)''', 
                    (piece['id'], gender_id, piece['accessionyear']))
        if cur.rowcount == 1:
            new_inserts += 1

    conn.commit()

    cur.execute('''SELECT COUNT(*) FROM HarvardArt''')
    num_of_art = cur.fetchone()[0]
    print(f"Pieces of art in HarvardArt table of Art database: {num_of_art}")

def create_met_directors_table(conn, cur):
    '''Creates the MetDirectors table within the database using the input connection (conn) and cursor (cur)'''
    cur.execute('''CREATE TABLE IF NOT EXISTS MetDirectors
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        start_year INTEGER,
        end_year INTEGER)'''
        )
    conn.commit()

def add_met_directors_from_json(conn, cur, filename):

    with open(filename, 'r') as file:
        content = json.load(file)

    for item in content:
        cur.execute('''INSERT OR IGNORE INTO MetDirectors (name,start_year,end_year) VALUES (?,?,?)''', 
        (item['name'], item['start_year'], item['end_year']))

    conn.commit()

def create_met_art_table(conn, cur):
    '''Creates the MetArt table within the database using the input connection (conn) and cursor (cur)'''
    cur.execute('''CREATE TABLE IF NOT EXISTS MetArt
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        objectID INTEGER UNIQUE,
        artistGender INTEGER,
        accessionYear INTEGER)''')
    conn.commit()

def add_met_art_from_json(conn, cur, filename):
    with open(filename, 'r') as file:
        content = json.load(file)

    cur.execute('''SELECT COUNT(*) FROM MetArt''')
    num_of_art = cur.fetchone()[0]

    new_inserts = 0
    for item in content:
        
        if num_of_art < 100:
            if new_inserts >= 25:
                break
        gender = item['artistGender']
        gender_id = cur.execute(f'''SELECT id FROM Genders 
        WHERE gender=?''', (f"{gender}",)).fetchall()
        gender_id_int = gender_id[0][0]

        cur.execute('''INSERT OR IGNORE INTO MetArt (objectID,artistGender,accessionYear) VALUES (?,?,?)''',
        (item['objectID'], gender_id_int, item['accessionYear']))

        if cur.rowcount == 1:
            new_inserts += 1

    conn.commit()

    cur.execute('''SELECT COUNT(*) FROM MetArt''')
    num_of_art = cur.fetchone()[0]
    print(f"Pieces of art in MetArt table of Art database: {num_of_art}")

def main():
    '''Sets up the database, adds all 5 tables and fills them with data from 4 JSON files'''
    conn, cur = set_up_database("Art.db")
    create_gender_table(conn, cur)
    create_harvard_directors_table(conn, cur)
    add_harvard_directors_from_json(conn, cur, "harvard_directors.json")
    create_harvard_art_table(conn, cur)
    #for i in range(33): #get rid of loop
    add_harvard_art_from_json(conn, cur, "harvard.json")
    create_met_directors_table(conn, cur)
    add_met_directors_from_json(conn, cur, "met_directors.json")
    create_met_art_table(conn, cur)
    #for i in range(4): #get rid of loop
    add_met_art_from_json(conn, cur, "met.json")

if __name__ == "__main__":
    main()

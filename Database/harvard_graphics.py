import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt



def art_by_accession_year(conn, cur):
    '''Creates a pie chart of number of pieces of art by gender at the Harvard Art Museums
    using data from the HarvardArt database
    
    Args:
        conn: connection to database
        cur: cursor
    
    Output:
        art_count_by_accession_year (dict): dictionary containing art count by accession year (ascending by chronological order)
    '''
    art_count_by_year = {}
    years = cur.execute('''SELECT accessionyear 
    FROM HarvardArt''').fetchall()
    for year in years:
        art_count_by_year[year[0]] = art_count_by_year.get(year[0], 0) + 1

    art_count_by_year = dict(sorted(art_count_by_year.items()))

    # Data for plotting
    y = list(art_count_by_year.keys())
    x = list(art_count_by_year.values())

    # create the line graph
    fig, ax = plt.subplots()
    ax.plot(y, x)
    ax.set_xlabel('Accession Year')
    ax.set_ylabel('Pieces of Art')
    ax.set_title('Amount of Art Acquired by Accession Year at the Harvard Art Museum')
    #ax.grid()

    # save the line graph
    fig.savefig("harvard_art_by_accession_year.png")

    # show the line graph
    plt.show()

    return art_count_by_year

def art_by_gender(conn, cur):
    '''Creates a line plot of amount of art by accession year
    using data from the HarvardArt database
    
    Args:
        conn: connection to database
        cur: cursor
    
    Output:
        (art_by_women, art_by_men_or_unknown) (tuple): tuple containing art count by gender
            art_by_women (tuple): (id of gender in database, count of art by women)
            art_by_men_or_unknown (tuple): (id of gender in database, count of art by men/unkown)
    '''
    #get the number of pieces of art by gender
    cur.execute('''SELECT Genders.id, COUNT(*)
    FROM Genders JOIN HarvardArt ON Genders.id = HarvardArt.artistGender
    WHERE gender = ?
    ''', ('Female',))
    art_by_women = cur.fetchone()
    #print(art_by_women)
    cur.execute('''SELECT Genders.id, COUNT(*)
    FROM Genders JOIN HarvardArt ON Genders.id = HarvardArt.artistGender
    WHERE gender = ?
    ''', ('Male/Unknown',))
    art_by_men_or_unknown = cur.fetchone()
    #print(art_by_men_or_unknown)

    #create the pie chart
    plt.figure(figsize=(8, 8))
    labels = ['Female Artists', 'Male/Unknown Artists']
    sizes = [art_by_women[1], art_by_men_or_unknown[1]]
    colors = ['lightcoral', 'lightskyblue']
    explode = (0.2, 0)
 
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=False, startangle=175)

    plt.axis('equal')
    plt.title('Harvard Art Museum Pieces by Artist Gender')

    # save the pie chart
    plt.savefig("harvard_art_by_gender.png")

    # show the pie chart
    plt.show()

    return (art_by_women, art_by_men_or_unknown)
    

def write_calulations(art_by_year, art_by_women, art_by_men_or_unknown):
    with open('calculations.txt', 'a') as f:
        f.write(f"Harvard Art Museums Calculations\n")
        f.write("\n")
        f.write(f"Harvard Art by Accession Year\n")
        for year, count in art_by_year.items():
            f.write(f"  {year}: {count}\n")
        f.write("\n")
        f.write("Harvard Art by Artist Gender\n")
        f.write(f"  Total Pieces of Art: {art_by_women[1]+art_by_men_or_unknown[1]}\n")
        f.write(f"    Male Artists: {art_by_men_or_unknown[1]}\n")
        f.write(f"    Female Artists: {art_by_women[1]}\n")
        f.write("\n")
    print("works")
    pass
    

def main(): 
    # create the connection and cursor for the Art database
    dir = os.path.dirname(__file__)+ os.sep
    conn = sqlite3.connect(dir+'Art.db')
    cur = conn.cursor()

    art_by_year = art_by_accession_year(conn, cur)
    art_by_women, art_by_men_or_unknown = art_by_gender(conn, cur)
    write_calulations(art_by_year, art_by_women, art_by_men_or_unknown)


if __name__ == '__main__':
    main()
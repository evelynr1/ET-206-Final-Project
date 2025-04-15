import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt



def art_by_accession_year(conn, cur):
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

def art_by_director(conn, cur):
    names = []
    director_dict = {}
    director_names = cur.execute('''SELECT name 
    FROM HarvardDirectors''').fetchall()
    for item in director_names:
        names.append(item[0])
    print(names)
    print(len(names))


    directors_all_art = cur.execute('''SELECT HD.name, COUNT(*) 
                        FROM HarvardDirectors HD
                        JOIN HarvardArt HA
                        ON HA.accessionYear BETWEEN HD.start_year AND HD.end_year
                        WHERE HA.artistGender IN (1,2)
                        GROUP BY HD.name, HA.artistGender;
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
    

    pass
    


def main(): 
    dir = os.path.dirname(__file__)+ os.sep
    conn = sqlite3.connect(dir+'Art.db')
    cur = conn.cursor()

    print(art_by_accession_year(conn, cur))
    #art_by_director(conn, cur)

if __name__ == '__main__':
    main()


# ####from class. make changes

# # Data for plotting
# y = []
# x = []

# # create the line graph
# fig, ax = plt.subplots()
# ax.pie(y, x)
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_title('title')
# #ax.grid()

# # save the line graph
# fig.savefig("test.png")

# # show the line graph
# plt.show()


# import matplotlib.pyplot as plt
 
# # Data to plot
# labels = ['Python', 'C++', 'Ruby', 'Java']
# sizes = [215, 130, 245, 210]
# colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
# explode = (0.1, 0, 0, 0)  # explode 1st slice
 
# # Plot
# plt.pie(sizes, explode=explode, labels=labels, colors=colors,
#         autopct='%1.1f%%', shadow=True, startangle=140)
 
# plt.axis('equal')
# plt.show()
import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt



def art_by_year(conn, cur):
    directors = {}
    names = cur.execute('''SELECT year 
    FROM MetDirectors''').fetchall()
    for item in director_names:
        names.append(item[0])
        names.append(item[0])
    print(names)
    print(len(names))
    pass
    


def main(): 
    dir = os.path.dirname(__file__)+ os.sep
    conn = sqlite3.connect(dir+'Art.db')
    cur = conn.cursor()

    art_by_year(conn, cur)


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
# testing sqlite3

import sqlite3

# create connection
con = sqlite3.connect("tutorial.db")

# create cursor
cur = con.cursor()

# create table
# use the .execute() cursor method to execute SQL statements

# create sample table
#cur.execute("DROP TABLE movie")
cur.execute("""CREATE TABLE IF NOT EXISTS movie(
            title TEXT, 
            year TEXT, 
            score TEXT)
            """)

# check that the table exists
table_check = cur.execute("SELECT name FROM sqlite_master")
table_names = table_check.fetchone()
print(type(table_names))
print("Table names: ",table_names)

# note that .fetchone() moves fetches the sql command AND moves cursor to next row
# running .fetchone() again and checking type results in NoneType if cursor is at end of file
#print(type(table_check.fetchone()))
#print(type(table_check))


# populate movie table (title, year, score)
cur.execute("""INSERT INTO movie VALUES
            ('Monty Python and the Holy Grail', 1972, 8.2),
            ('And Now for Something Completely Different', 1971, 7.5)
            """)

# INSERT implicitly creates a transaction
# commit transaction
con.commit()

# query table
cur.execute("SELECT * FROM movie")
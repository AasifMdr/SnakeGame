import sqlite3

conn=sqlite3.connect("UserDatabase.db")
c=conn.cursor()
c.execute(
    '''CREATE TABLE user_details(
        username text,
        password text,
        highscore integer
    ) '''
)

conn.commit()
conn.close()
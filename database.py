import sqlite3 as lite


def db_open(filename):
    "Opens and close the database"
    data = (,)
    with lite.connect(filename) as conn:
        print(f"I created my database named {filename}")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        data = (row for row in cursor.fetchall())


db_open("db1.db")
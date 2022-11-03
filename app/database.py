import sqlite3 as sql
import os
from sqlite3 import Error

def initDatabase():
    if os.path.exists("database.db"):
        os.remove("database.db")

    connection = sql.connect("database.db")
    with open("tables.sql") as f:
        connection.executescript(f.read())

    connection.commit()
    connection.close()

if __name__ == '__main__':
    initDatabase()

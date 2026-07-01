import sqlite3

conn = sqlite3.connect("bank.db")
cusror = conn.cursor()

cusror.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT )
""")

conn.commit ()
conn.close ()

print("Database Created")
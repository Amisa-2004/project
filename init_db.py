# for creating the database tables
import sqlite3

with open ('schema.sql') as f:
    schema  = f.read()

conn = sqlite3.connect('pyqs.db')
conn.executescript(schema)
conn.close

print("Database and table created successfully")
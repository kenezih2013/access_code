import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Test data
cur.execute("INSERT INTO posts (guest_name, host_address, access_code) VALUES (?, ?, ?)",
            ('Jude Samson', '12, King Haggai Rd', 51232)
            )

cur.execute("INSERT INTO users (full_name, resident_address, email, validity_date) VALUES (?, ?, ?, ?)",
            ('Taiwo Samson', '5, Nduma Kalu  Rd', 'taiwo.samson@gmail.com', '2024-08-20')
            )

connection.commit()
connection.close()
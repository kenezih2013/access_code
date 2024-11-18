import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Test data

cur.execute("INSERT INTO admin_users (full_name, a_address, email, a_profile, validity_date) VALUES (?, ?, ?, ?, ?)",
            ('Kenneth Ezih', '1, CCC Edidi Ave', 'kenezih@gmail.com', 'super admin', '2099-12-31')
            )

#cur.execute("INSERT INTO posts (guest_name, host_address, access_code, user_id) VALUES (?, ?, ?, ?)",
#            ('Jude Samson', '12, King Haggai Rd', 51232, 1)
#            )

connection.commit()
connection.close()
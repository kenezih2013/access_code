import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Test data

cur.execute("INSERT INTO admin_users (full_name, a_address, email, a_profile, validity_date) VALUES (?, ?, ?, ?, ?)",
            ('Kenneth Ezih', '1, CCC Edidi Ave', 'kenezih@gmail.com', 'super admin', '2099-12-31')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('5', 'Oladiji Olojo',	'5 George Amurun Street', 'oladijiolojo@gmail.com', '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('6', 'William F. Ogundiran',	'13 Abiodun Bada', 'wfogundiran@gmail.com', '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('7', 'Kayode Adebiyi',	'8 Joe Akonobi', 'kydadebiyi@yahoo.com', '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('8', 'Olufunke Ogunmoyero',	'1 Alonge Ogunmoyero Close', 'olu04@yahoo.com', '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('9', 'Shegun Odebunmi',	'13 Uduma Kalu', 'shegun.odebunmi@gmail.com',  '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('10', 'Taiwo Samson',	'8 Olutayo Alao ', 'taiwosamlekan@gmail.com',  '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('11', 'Okunlola Eunice',	'19 Olutayo Alao',	'okunlolaeunice@gmail.com',  '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('12', 'Bolarinwa Opeyemi',	'10 Edidi Avenue',	'rasaqopeyemi@yahoo.com', '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('13', 'Osato Osawaye',	'18/20 Kayode Anifowose',	'osatoosawaye@gmail.com', '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('14', 'Abe Oluwaseyi',	'4 Alonge Ogunmoyero Close',	'oluwaseyiabe@hotmail.com', '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('15', 'Olabiran Kayode',	'3 King Haggai Street',	'kayolab@gmail.com', '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('16', 'Onyekachi Nwosu Conel',	'3 Abiodun Bada Crescent',	'cuteconel@yahoo.com', '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('17', 'Olaberinjo Francis',	'5 Uduma Kalu',	'olaberinjo@yahoo.com', '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('18', 'Chima Nwankwo', '6, Edidi Ave.', 'kachrlg@yahoo.com', '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('19', 'Richard N. Chime',	'12B, Uduma Kalu Drive',	'richnnachime@yahoo.com', '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('20', 'Amure Morayo Abiodun',	'9, Joe Akonobi',	'morayo23rd4real@gmail.com', '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('21', 'Tolani Olatunde Awere',	'4C, George Amuren',	'tolawere@gmail.com', '2025-12-31', '2024-12-23')
            )

cur.execute("INSERT INTO users (user_id, full_name, resident_address, email, validity_date, u_created) VALUES (?, ?, ?, ?, ?, ?)",
            ('22', 'Animashaun Oladimeji',	'5A, Joe Akonobi',	'oasanimashaun@gmail.com', '2025-12-31', '2024-12-23')
            )


#cur.execute("INSERT INTO posts (guest_name, host_address, access_code, user_id) VALUES (?, ?, ?, ?)",
#            ('Jude Samson', '12, King Haggai Rd', 51232, 1)
#            )

connection.commit()
connection.close()
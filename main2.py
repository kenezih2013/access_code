import sqlite3
import pandas as pd
#import main

#main = (__name__)

conn = sqlite3.connect('database.db')
c = conn.cursor()
df = pd.read_csv("access_code_admins.csv")
df.to_sql('admin_users', conn, if_exists='append', index = False, chunksize = 10000)

if __name__ == '__main__':
    main2()

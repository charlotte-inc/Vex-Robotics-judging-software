import pandas as pd
import sqlite3

db = r'judging_database.db'

def sql_read(sql):
    conn = sqlite3.connect(db)
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

def sql_execute(sql):
    a = True
    while a:
        #print('sql_execute')
        #try:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()   
            a = False
        #except:
        #    print('trying again')
    #print('')
    return 
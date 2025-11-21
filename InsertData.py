import sqlite3
databaseLoc = 'myTest.db'

conn = sqlite3.connect(databaseLoc)
cursor = conn.cursor()

with open('DATA/cyber_incidents.csv') as cyber:
    i = 0
    for line in cyber.readlines():
        if i == 0:
            i+=1
            continue
        line = line.strip()
        vals = line.split(',')
        #vals[0],vals[1],vals[2],vals[3],vals[4],vals[5]
        #incident_id, timestamp
        insertScript = """insert into cyber_incidents(id,i_date,i_type,status,description,reported_by)
                       values(?,?,?,?,?,?,?)"""
        cursor.execute(insertScript, vals)
        conn.commit()

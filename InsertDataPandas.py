import pandas as pd
import sqlite3


df = pd.read_csv('Data/cyber_incidents.csv')

print(df.head())
print(df.describe())

databaseLoc = 'cyber_incidents.db'
conn = sqlite3.connect(databaseLoc)
cursor = conn.cursor()
df.to_sql('cyber_incidents', conn, if_exists='append', index=False)
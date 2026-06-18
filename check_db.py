import sqlite3
import pandas as pd

conn = sqlite3.connect("grants.db")

df = pd.read_sql(
    "SELECT * FROM grants_new LIMIT 10",
    conn
)

print(df)

conn.close()
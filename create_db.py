import sqlite3
import pandas as pd

df = pd.read_csv("grants.csv")

print(df.head())

conn = sqlite3.connect("grants.db")

df.to_sql(
    "grants",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Database created successfully!")
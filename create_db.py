import sqlite3
import pandas as pd

def create_database():
    df = pd.read_csv("grants.csv")

    conn = sqlite3.connect("grants.db")

    df.to_sql(
        "grants_new",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("Database created successfully")
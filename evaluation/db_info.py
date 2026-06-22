import sqlite3
import pandas as pd

conn = sqlite3.connect("grants.db")

# Get all table names
tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';",
    conn
)

print("\n========== DATABASE TABLES ==========")
print(tables)

# Inspect each table
for table in tables["name"]:

    print(f"\n========== {table.upper()} ==========")

    # Total rows
    count = pd.read_sql(
        f"SELECT COUNT(*) AS total_rows FROM {table};",
        conn
    )

    print("\nTotal Rows:")
    print(count)

    # First 5 rows
    df = pd.read_sql(
        f"SELECT * FROM {table} LIMIT 5;",
        conn
    )

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 Rows:")
    print(df)

conn.close()
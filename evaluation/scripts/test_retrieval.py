from app import calculate_matches
import pandas as pd

df = pd.read_sql(
    "SELECT * FROM grants_new",
    "sqlite:///grants.db"
)

query = "We provide STEM education for underserved students."

results = calculate_matches(query, df)

print("=" * 50)

for rank, result in enumerate(results, start=1):
    print(rank, result[0], round(result[1], 4))
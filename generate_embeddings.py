import sqlite3
import pandas as pd
import json

from sentence_transformers import SentenceTransformer

def generate_embeddings():

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    conn = sqlite3.connect("grants.db")

    df = pd.read_sql(
        "SELECT * FROM grants_new",
        conn
    )

    embeddings = []

    for _, row in df.iterrows():

        embedding = model.encode(
            row["description"]
        )

        embeddings.append(
            json.dumps(
                embedding.tolist()
            )
        )

    df["embedding"] = embeddings

    df.to_sql(
        "grants_new",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("Embeddings generated!")
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000/analyze"

df = pd.read_csv("data/fake_job_postings.csv")

for idx, row in df.sample(5).iterrows():
    description = row["description"]
    label = row["fraudulent"]

    response = requests.post(API_URL, json={"description": description})

    print(f"\nJob Title: {row['title']}")
    print(f"True Label: {'fake' if label == 1 else 'legit'}")
    print(f"API Response: {response.json()}")
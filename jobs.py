import json
import pandas as pd

# Load keywords
with open("keywords.txt", "r", encoding="utf-8") as f:
    keywords = [k.strip().lower() for k in f if k.strip()]

# Load ignored words
with open("ignore.txt", "r", encoding="utf-8") as f:
    ignored = [k.strip().lower() for k in f if k.strip()]

# Load bank list
with open("banks.json", "r", encoding="utf-8") as f:
    banks = json.load(f)

# --------------------------------------------------
# Temporary sample data
# (Later we'll replace this with live bank collectors)
# --------------------------------------------------

sample_jobs = [
    {
        "company": "Mashreq",
        "title": "Assistant Manager - Credit Cards Retention",
        "location": "Bengaluru",
        "mode": "Remote",
        "url": "https://example.com/job1"
    },
    {
        "company": "Mashreq",
        "title": "Java Developer",
        "location": "Bengaluru",
        "mode": "Remote",
        "url": "https://example.com/job2"
    }
]

results = []

for job in sample_jobs:
    title = job["title"].lower()

    if any(word in title for word in ignored):
        continue

    if any(word in title for word in keywords):
        results.append(job)

df = pd.DataFrame(results)

if len(df):
    df.to_csv("jobs.csv", index=False)
    print(df)
else:
    print("No matching jobs found.")

import json
import os
import pandas as pd

from notifier import send_job
from collectors.remoteok import fetch_jobs

# Load keywords
with open("keywords.txt", "r", encoding="utf-8") as f:
    keywords = [k.strip().lower() for k in f if k.strip()]

# Load ignored words
with open("ignore.txt", "r", encoding="utf-8") as f:
    ignored = [k.strip().lower() for k in f if k.strip()]

# Load banks (we'll use this later)
with open("banks.json", "r", encoding="utf-8") as f:
    banks = json.load(f)

print("Fetching jobs from Remote OK...")

try:
    all_jobs = fetch_jobs()
except Exception as e:
    print("Error fetching jobs:", e)
    all_jobs = []

results = []
posted_file = "data/posted_jobs.json"

if os.path.exists(posted_file):
    with open(posted_file, "r", encoding="utf-8") as f:
        posted_jobs = json.load(f)
else:
    posted_jobs = []
for job in all_jobs:
    title = job.get("title", "").lower()
    company = job.get("company", "").lower()
    tags = " ".join(job.get("tags", [])).lower()

    # Skip unwanted jobs
    if any(word in title for word in ignored):
        continue

    # Keep only banking/finance related jobs
    matched = (
        any(word in title for word in keywords)
        or any(word in tags for word in keywords)
        or any(bank["name"].lower() in company for bank in banks)
    )

    if matched:
        job_data = {
    "company": job["company"],
    "title": job["title"],
    "location": job["location"],
    "mode": job["mode"],
    "link": job["link"],
    "date": job["date"]
}

job_id = f"{job_data['company']}|{job_data['title']}|{job_data['link']}"

if job_id not in posted_jobs:
    results.append(job_data)
    

df = pd.DataFrame(results)

if not df.empty:

    # Send each job to Telegram
    for job in results:
        send_job(job)

    # Save CSV
    df.to_csv("data/jobs.csv", index=False)

    print(df)
    print(f"\nFound {len(df)} matching jobs.")

else:
    print("No matching banking jobs found.")

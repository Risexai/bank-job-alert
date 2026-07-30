import json
import os
import pandas as pd

from notifier import send_job
from collectors.remoteok import fetch_jobs as remoteok_jobs
from collectors.remotive import fetch_jobs as remotive_jobs

# Load keywords
with open("keywords.txt", "r", encoding="utf-8") as f:
    keywords = [k.strip().lower() for k in f if k.strip()]

# Load ignored words
with open("ignore.txt", "r", encoding="utf-8") as f:
    ignored = [k.strip().lower() for k in f if k.strip()]

# Load banks
with open("banks.json", "r", encoding="utf-8") as f:
    banks = json.load(f)

posted_file = "data/posted_jobs.json"

if os.path.exists(posted_file):
    with open(posted_file, "r", encoding="utf-8") as f:
        posted_jobs = json.load(f)
else:
    posted_jobs = []

print("Fetching jobs from Remote OK...")

try:
    all_jobs = []

all_jobs.extend(remoteok_jobs())
all_jobs.extend(remotive_jobs())
except Exception as e:
    print("Error fetching jobs:", e)
    all_jobs = []

results = []

for job in all_jobs:

    title = job.get("title", "").lower()
    company = job.get("company", "").lower()
    tags = " ".join(job.get("tags", [])).lower()

    if any(word in title for word in ignored):
        continue

    matched = (
        any(word in title for word in keywords)
        or any(word in tags for word in keywords)
        or any(bank["name"].lower() in company for bank in banks)
    )

    if not matched:
        continue

    job_data = {
        "company": job.get("company", ""),
        "title": job.get("title", ""),
        "location": job.get("location", ""),
        "mode": job.get("mode", "Remote"),
        "link": job.get("link", ""),
        "date": job.get("date", "")
    }

    job_id = f"{job_data['company']}|{job_data['title']}|{job_data['link']}"

    if job_id in posted_jobs:
        continue

    results.append(job_data)
    posted_jobs.append(job_id)

df = pd.DataFrame(results)

if not df.empty:

    for job in results:
        send_job(job)

    df.to_csv("data/jobs.csv", index=False)

    with open(posted_file, "w", encoding="utf-8") as f:
        json.dump(posted_jobs, f, indent=2)

    print(df)
    print(f"Found {len(df)} new jobs.")

else:
    print("No new jobs found.")

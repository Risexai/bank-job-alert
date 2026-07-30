import json

from config import ENABLE_REMOTEOK, ENABLE_REMOTIVE
from storage import load_posted_jobs, save_posted_jobs, save_jobs
from filters import is_matching, is_ignored
from notifier import send_job

from collectors.remoteok import fetch_jobs as remoteok_jobs
from collectors.remotive import fetch_jobs as remotive_jobs


# -----------------------
# Load configuration files
# -----------------------

with open("keywords.txt", "r", encoding="utf-8") as f:
    keywords = [x.strip().lower() for x in f if x.strip()]

with open("ignore.txt", "r", encoding="utf-8") as f:
    ignored = [x.strip().lower() for x in f if x.strip()]

with open("banks.json", "r", encoding="utf-8") as f:
    banks = json.load(f)


posted_jobs = load_posted_jobs()

all_jobs = []

# -----------------------
# Collect Jobs
# -----------------------

if ENABLE_REMOTEOK:
    try:
        print("Loading Remote OK...")
        all_jobs.extend(remoteok_jobs())
    except Exception as e:
        print("Remote OK:", e)

if ENABLE_REMOTIVE:
    try:
        print("Loading Remotive...")
        all_jobs.extend(remotive_jobs())
    except Exception as e:
        print("Remotive:", e)


# -----------------------
# Filter Jobs
# -----------------------

results = []

for job in all_jobs:

    title = job.get("title", "")

    if is_ignored(title, ignored):
        continue

    if not is_matching(job, keywords, banks):
        continue

    job_id = f"{job.get('company')}|{job.get('title')}|{job.get('link')}"

    if job_id in posted_jobs:
        continue

    results.append(job)
    posted_jobs.append(job_id)


# -----------------------
# Telegram
# -----------------------

for job in results:
    send_job(job)


# -----------------------
# Save Files
# -----------------------

save_jobs(results)
save_posted_jobs(posted_jobs)

print(f"Finished. {len(results)} new jobs.")

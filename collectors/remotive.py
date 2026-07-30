import requests

REMOTIVE_URL = "https://remotive.com/api/remote-jobs"

def fetch_jobs():
    response = requests.get(REMOTIVE_URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    jobs = []

    for job in data.get("jobs", []):

        jobs.append({
            "company": job.get("company_name", ""),
            "title": job.get("title", ""),
            "location": job.get("candidate_required_location", "Remote"),
            "mode": "Remote",
            "link": job.get("url", ""),
            "date": job.get("publication_date", ""),
            "tags": job.get("tags", [])
        })

    return jobs

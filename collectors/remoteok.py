import requests

REMOTEOK_URL = "https://remoteok.com/api"

def fetch_jobs():
    headers = {
        "User-Agent": "RiseX-Bank-Job-Alert/1.0"
    }

    response = requests.get(REMOTEOK_URL, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()

    jobs = []

    # First element contains metadata, skip it
    for job in data[1:]:
        title = job.get("position", "")
        company = job.get("company", "")
        location = job.get("location", "Remote")
        link = job.get("url", "")
        date = job.get("date", "")
        tags = job.get("tags", [])

        jobs.append({
            "company": company,
            "title": title,
            "location": location,
            "mode": "Remote",
            "link": link,
            "date": date,
            "tags": tags
        })

    return jobs

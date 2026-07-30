import json
import os
import pandas as pd

from config import POSTED_FILE, CSV_FILE


def load_posted_jobs():

    if os.path.exists(POSTED_FILE):
        with open(POSTED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    return []


def save_posted_jobs(posted):

    with open(POSTED_FILE, "w", encoding="utf-8") as f:
        json.dump(posted, f, indent=2)


def save_jobs(jobs):

    df = pd.DataFrame(jobs)

    if not df.empty:
        df.to_csv(CSV_FILE, index=False)

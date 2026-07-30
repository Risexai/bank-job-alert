import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_job(job):

    company = job.get("company", "Unknown")
    title = job.get("title", "Unknown")
    location = job.get("location", "Remote")
    mode = job.get("mode", "Remote")
    link = job.get("link", "")
    date = job.get("date", "Today")

    message = f"""
🏦 <b>REMOTE BANKING JOB</b>

💼 <b>Role</b>
{title}

🏢 <b>Company</b>
{company}

📍 <b>Location</b>
{location}

🏠 <b>Work Mode</b>
{mode}

📅 <b>Posted</b>
{date}

🔗 <b>Apply Now</b>
{link}

━━━━━━━━━━━━━━━━━━━

📢 <b>Join @India_JobAlerts26</b>

#RemoteJobs #BankJobs #HybridJobs #WFHJobs
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }

    response = requests.post(url, data=payload, timeout=30)

    print(response.text)

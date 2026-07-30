import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_job(job):
    message = f"""
🏦 <b>Remote Banking Job</b>

🏢 <b>Company:</b> {job['company']}

💼 <b>Role:</b>
{job['title']}

📍 <b>Location:</b>
{job['location']}

🏠 <b>Mode:</b>
{job['mode']}

🔗 <b>Apply:</b>
{job['link']}

━━━━━━━━━━━━━━
📢 Join @IndiaJobAlerts26
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    requests.post(url, data=payload)

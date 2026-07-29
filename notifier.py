import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

message = """
🏦 <b>Bank Job Alert Test</b>

✅ Congratulations!

Your Telegram integration is working successfully.

Next, we'll send real jobs from Mashreq and other banks automatically.

- RiseX AI Banking Job Hunter
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "HTML"
}

response = requests.post(url, data=payload)

print(response.text)

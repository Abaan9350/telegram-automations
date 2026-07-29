from dotenv import load_dotenv
import os
import requests

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

from datetime import date

today = date.today().strftime("%Y-%m-%d")

wordle_url = f"https://www.nytimes.com/svc/wordle/v2/{today}.json"

wordle = requests.get(wordle_url).json()

answer = wordle["solution"].upper()

payload = {
    "chat_id": CHAT_ID,
    "text": f"🟩 Today's Wordle answer: {answer}"
}

response = requests.post(url, data=payload)

print(response.json())
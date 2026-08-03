import os
import json
import httpx
import time

STATE_FILE = "state/btc_alert_state.json"
from config import BTC_ALERT_THRESHOLD
from config import REQUEST_TIMEOUT


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"alerted": False}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def get_btc_price_and_change():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "x_cg_demo_api_key": os.environ["COINGECKO_API_KEY"],
    }

    with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
        for attempt in range(3):
            resp = client.get(url, params=params)

            if resp.status_code == 429 and attempt < 2:
                time.sleep(2 ** attempt)
                continue

            resp.raise_for_status()
            break

    data = resp.json()["bitcoin"]
    return data["usd"], data["usd_24h_change"]


def send_telegram_message(text):
    bot_token = os.environ["BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    with httpx.Client(timeout=10) as client:
        resp = client.post(
            url,
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            }
        )

        if resp.status_code >= 400:
            print(f"Telegram API error response: {resp.text}")

        resp.raise_for_status()


def main():
    # Detect how the workflow was started
    event = os.getenv("GITHUB_EVENT_NAME")

    # Send a confirmation only when you manually click "Run workflow"
    if event == "workflow_dispatch":
        send_telegram_message("🧪 *BTC Price Alert workflow executed successfully!*")

    price, change = get_btc_price_and_change()

    state = load_state()

    crossed = abs(change) >= BTC_ALERT_THRESHOLD

    if crossed and not state.get("alerted", False):
        direction = "📈" if change > 0 else "📉"

        send_telegram_message(
            f"{direction} *Bitcoin Price Alert!*\n\n"
            f"📊 *24h Change:* `{change:+.2f}%`\n"
            f"💰 *Current Price:* `${price:,.2f}`"
        )

        state["alerted"] = True
        save_state(state)

    elif not crossed and state.get("alerted", False):
        # Reset so the next threshold crossing sends a notification again
        state["alerted"] = False
        save_state(state)


if __name__ == "__main__":
    main()
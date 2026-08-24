import os
import json
import httpx
import time

from config import BTC_ALERT_THRESHOLD
from config import REQUEST_TIMEOUT


STATE_FILE = "state/btc_alert_state.json"

# Minimum time between Bitcoin alerts
COOLDOWN_SECONDS = 24 * 60 * 60


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)

    return {"last_alert_at": 0}


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
    }
    # Add API key if available (optional for public API)
    api_key = os.getenv("COINGECKO_API_KEY")
    if api_key:
        params["x_cg_demo_api_key"] = api_key

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
                "disable_web_page_preview": True,
            },
        )

        if resp.status_code >= 400:
            print(f"Telegram API error response: {resp.text}")

        resp.raise_for_status()


def main():
    # Detect how the workflow was started
    event = os.getenv("GITHUB_EVENT_NAME")

    # Send a confirmation only when manually triggered
    if event == "workflow_dispatch":
        send_telegram_message(
            "🧪 *BTC Price Alert workflow executed successfully!*"
        )

    price, change = get_btc_price_and_change()

    state = load_state()

    # Check whether Bitcoin has crossed the configured threshold
    crossed = abs(change) >= BTC_ALERT_THRESHOLD

    # Current time
    now = time.time()

    # Time when the previous alert was sent
    last_alert_at = state.get("last_alert_at", 0)

    # Check whether the 24-hour cooldown has expired
    cooldown_over = (now - last_alert_at) >= COOLDOWN_SECONDS

    # Send an alert only when:
    # 1. Bitcoin is currently above/below the configured threshold
    # 2. At least 24 hours have passed since the previous alert
    if crossed and cooldown_over:
        direction = "📈" if change > 0 else "📉"

        send_telegram_message(
            f"{direction} *Bitcoin Price Alert!*\n\n"
            f"📊 *24h Change:* `{change:+.2f}%`\n"
            f"💰 *Current Price:* `${price:,.2f}`"
        )

        # Record the exact time the alert was sent
        state["last_alert_at"] = now
        save_state(state)

        print("BTC alert sent successfully.")

    else:
        if not crossed:
            print(
                f"Threshold not crossed. "
                f"Current 24h change: {change:+.2f}%"
            )
        else:
            remaining = COOLDOWN_SECONDS - (now - last_alert_at)
            remaining_hours = remaining / 3600

            print(
                f"Threshold crossed, but cooldown is active. "
                f"Approximately {remaining_hours:.1f} hours remaining."
            )


if __name__ == "__main__":
    main()
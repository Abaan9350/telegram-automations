import os
import json
import httpx

STATE_FILE = "state/btc_alert_state.json"
THRESHOLD_PCT = 1.0

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
    params = {"ids": "bitcoin", "vs_currencies": "usd", "include_24hr_change": "true"}
    with httpx.Client(timeout=10) as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()
    data = resp.json()["bitcoin"]
    return data["usd"], data["usd_24h_change"]

def send_telegram_message(text):
    bot_token = os.environ["BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    with httpx.Client(timeout=10) as client:
        resp = client.post(url, json={"chat_id": chat_id, "text": text})
        resp.raise_for_status()

def main():
    price, change = get_btc_price_and_change()
    state = load_state()
    crossed = abs(change) >= THRESHOLD_PCT

    if crossed and not state["alerted"]:
        direction = "📈" if change > 0 else "📉"
        send_telegram_message(
            f"{direction} Bitcoin moved {change:+.2f}% in the last 24h\n"
            f"Current price: ${price:,.2f}"
        )
        state["alerted"] = True
        save_state(state)
    elif not crossed and state["alerted"]:
        state["alerted"] = False  # reset, so the next crossing can alert again
        save_state(state)

if __name__ == "__main__":
    main()
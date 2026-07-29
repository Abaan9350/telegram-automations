import os
import json
import httpx

STATE_FILE = "state/epic_alert_state.json"
EPIC_URL = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"titles": []}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def extract_free_games(data):
    elements = data["data"]["Catalog"]["searchStore"]["elements"]
    free_games = []

    for game in elements:
        # Check for active promotions
        promotions = game.get("promotions") or {}
        offers = promotions.get("promotionalOffers") or []

        if not offers:
            continue

        # Check if the game is actually free
        total_price = (game.get("price") or {}).get("totalPrice", {})
        if total_price.get("discountPrice", -1) != 0:
            continue

        # Get the store slug
        slug = game.get("productSlug")

        if not slug:
            mappings = game.get("offerMappings") or []
            if mappings:
                slug = mappings[0].get("pageSlug")

        url = (
            f"https://store.epicgames.com/en-US/p/{slug}"
            if slug
            else "https://store.epicgames.com/en-US/free-games"
        )

        free_games.append({
            "title": game["title"],
            "url": url,
        })

    return free_games
def send_telegram_message(text):
    bot_token = os.environ["BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    with httpx.Client(timeout=10) as client:
        resp = client.post(url, json={"chat_id": chat_id, "text": text})
        if resp.status_code >= 400:
            print(f"Telegram API error response: {resp.text}")
        resp.raise_for_status()

def main():
    with httpx.Client(timeout=10) as client:
        resp = client.get(EPIC_URL)
        resp.raise_for_status()
    games = extract_free_games(resp.json())

    current_titles = sorted(g["title"] for g in games)
    state = load_state()

    if current_titles != state["titles"]:
        if games:
            lines = ["🎮 New free games on Epic Games Store:"]
            for g in games:
                lines.append(f"• {g['title']}\n  {g['url']}")
            send_telegram_message("\n".join(lines))
        state["titles"] = current_titles
        save_state(state)

if __name__ == "__main__":
    main()
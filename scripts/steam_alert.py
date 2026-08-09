import os
import json
import re
import html
import httpx


STATE_FILE = "state/steam_alert_state.json"

STEAM_URL = (
    "https://store.steampowered.com/search/"
    "?hwtype=0&maxprice=free&category1=998&specials=1&ndl=1"
)


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    return {
        "app_ids": []
    }


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def extract_free_games(page_html):
    games = []

    # Find Steam search result rows.
    # Lookaheads are used because Steam can change
    # the order of HTML attributes.
    row_pattern = re.compile(
        r'<a\b'
        r'(?=[^>]*class="[^"]*search_result_row[^"]*")'
        r'(?=[^>]*data-ds-appid="([^"]+)")'
        r'(?=[^>]*href="([^"]+)")'
        r'[^>]*>'
        r'(.*?)'
        r'</a>',
        re.IGNORECASE | re.DOTALL
    )

    for match in row_pattern.finditer(page_html):
        app_id = match.group(1).split(",")[0]
        url = html.unescape(match.group(2))
        content = match.group(3)

        # Only keep games that are 100% discounted
        if not re.search(
            r'data-discount="100"',
            content,
            re.IGNORECASE
        ):
            continue

        if not re.search(
            r'data-price-final="0"',
            content,
            re.IGNORECASE
        ):
            continue

        # Extract title
        title_match = re.search(
            r'<span class="title">\s*(.*?)\s*</span>',
            content,
            re.IGNORECASE | re.DOTALL
        )

        if not title_match:
            continue

        title = re.sub(
            r"<[^>]+>",
            "",
            title_match.group(1)
        )

        title = html.unescape(title).strip()

        # Extract original price
        original_price_match = re.search(
            r'<div class="discount_original_price">\s*(.*?)\s*</div>',
            content,
            re.IGNORECASE | re.DOTALL
        )

        original_price = ""

        if original_price_match:
            original_price = re.sub(
                r"<[^>]+>",
                "",
                original_price_match.group(1)
            )

            original_price = html.unescape(
                original_price
            ).strip()

        # Extract final price
        final_price_match = re.search(
            r'<div class="discount_final_price">\s*(.*?)\s*</div>',
            content,
            re.IGNORECASE | re.DOTALL
        )

        final_price = "FREE"

        if final_price_match:
            final_price = re.sub(
                r"<[^>]+>",
                "",
                final_price_match.group(1)
            )

            final_price = html.unescape(
                final_price
            ).strip()

        # Remove Steam tracking parameters
        clean_url = url.split("?")[0]

        if app_id and title:
            games.append({
                "app_id": app_id,
                "title": title,
                "original_price": original_price,
                "final_price": final_price,
                "url": clean_url,
            })

    # Remove duplicates
    unique_games = {}

    for game in games:
        unique_games[game["app_id"]] = game

    return list(unique_games.values())


def send_telegram_message(text, chat_id):
    bot_token = os.environ["BOT_TOKEN"]

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    with httpx.Client(timeout=10) as client:
        response = client.post(
            url,
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True,
            },
        )

        if response.status_code >= 400:
            print(response.text)

        response.raise_for_status()


def main():
    event = os.getenv("GITHUB_EVENT_NAME")

    # Optional manual test confirmation
    if event == "workflow_dispatch":
        chat_ids = os.environ[
            "STEAM_GAMES_CHAT_IDS"
        ].split(",")

        for chat_id in chat_ids:
            send_telegram_message(
                "🧪 *Steam Games workflow executed successfully!*",
                chat_id.strip(),
            )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    # Fetch Steam
    with httpx.Client(
        timeout=10,
        headers=headers,
        follow_redirects=True,
    ) as client:
        response = client.get(STEAM_URL)
        response.raise_for_status()

    games = extract_free_games(response.text)

    print(f"Found {len(games)} free Steam games.")

    for game in games:
        print(
            f"- {game['title']} "
            f"({game['app_id']})"
        )

    # Load previous state
    state = load_state()

    previous_app_ids = set(
        state.get("app_ids", [])
    )

    current_app_ids = {
        game["app_id"]
        for game in games
    }

    # FIRST RUN:
    # Save the current games but don't alert.
    if not previous_app_ids:
        print(
            "No previous Steam state found. "
            "Initializing state without sending alerts."
        )

        state["app_ids"] = sorted(current_app_ids)
        save_state(state)
        return

    # Find genuinely new games
    new_app_ids = current_app_ids - previous_app_ids

    if new_app_ids:
        new_games = [
            game
            for game in games
            if game["app_id"] in new_app_ids
        ]

        lines = [
            "🚨 *New Steam Free Game!*",
            "",
        ]

        for game in new_games:
            lines.append(
                f"🎮 *{game['title']}*\n"
                f"💰 Was: {game['original_price']} → *FREE*\n"
                f"🔗 {game['url']}\n"
            )

        lines.append("🎉 *Happy Gaming!*")

        chat_ids = os.environ[
            "STEAM_GAMES_CHAT_IDS"
        ].split(",")

        message = "\n".join(lines)

        for chat_id in chat_ids:
            send_telegram_message(
                message,
                chat_id.strip()
            )

        print(
            f"Sent alert for {len(new_games)} new game(s)."
        )

    else:
        print("No new Steam games.")

    # Always update state
    state["app_ids"] = sorted(current_app_ids)
    save_state(state)


if __name__ == "__main__":
    main()
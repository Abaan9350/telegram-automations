import re
import html
import httpx

from telegram import Update
from telegram.ext import ContextTypes

from users import save_user
from notify import notify_admin
from . import command


STEAM_URL = (
    "https://store.steampowered.com/search/"
    "?hwtype=0&maxprice=free&category1=998&specials=1&ndl=1"
)


def extract_free_games(page_html):
    games = []

    # Find each Steam search result
    pattern = re.compile(
        r'<a\b'
        r'(?=[^>]*class="[^"]*search_result_row[^"]*")'
        r'(?=[^>]*href="([^"]+)")'
        r'(?=[^>]*data-ds-appid="([^"]+)")'
        r'[^>]*>'
        r'[\s\S]*?'
        r'<span class="title">([\s\S]*?)</span>'
        r'[\s\S]*?'
        r'<div class="discount_block[^>]*'
        r'data-price-final="0"[^>]*'
        r'data-discount="100"'
        r'[\s\S]*?'
        r'<div class="discount_original_price">([\s\S]*?)</div>'
        r'[\s\S]*?'
        r'<div class="discount_final_price">([\s\S]*?)</div>'
        r'[\s\S]*?</a>',
        re.IGNORECASE
    )

    for match in pattern.finditer(page_html):
        url = html.unescape(match.group(1))
        app_id = match.group(2).split(",")[0]

        title = re.sub(r"<[^>]+>", "", match.group(3))
        title = html.unescape(title).strip()

        original_price = re.sub(r"<[^>]+>", "", match.group(4))
        original_price = html.unescape(original_price).strip()

        final_price = re.sub(r"<[^>]+>", "", match.group(5))
        final_price = html.unescape(final_price).strip()

        if not app_id or not title:
            continue

        # Remove unnecessary Steam tracking parameters
        url = url.split("?")[0]

        games.append({
            "app_id": app_id,
            "title": title,
            "original_price": original_price,
            "final_price": final_price,
            "url": url,
        })

    return games


async def fetch_free_games():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    async with httpx.AsyncClient(
        timeout=10,
        headers=headers,
        follow_redirects=True,
    ) as client:
        response = await client.get(STEAM_URL)
        response.raise_for_status()

        return extract_free_games(response.text)


@command("steamgames", "Get currently free Steam games")
async def steamgames(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_new = save_user(update.effective_user)

    await notify_admin(
        context,
        update.effective_user,
        "/steamgames",
        is_new
    )

    try:
        games = await fetch_free_games()

        if not games:
            await update.message.reply_text(
                "🎮 No Steam games are currently 100% free."
            )
            return

        lines = [
            "🎮 *Steam Free Games*",
            "",
            f"🎁 *{len(games)} game(s) currently free:*",
            "",
        ]

        for i, game in enumerate(games, 1):
            lines.append(
                f"*{i}. {game['title']}*\n"
                f"💰 {game['original_price']} → *FREE*\n"
                f"🔗 {game['url']}\n"
            )

        lines.append("🎉 *Happy Gaming!*")

        await update.message.reply_text(
            "\n".join(lines),
            parse_mode="Markdown",
            disable_web_page_preview=True,
        )

    except httpx.HTTPStatusError:
        await update.message.reply_text(
            "⚠️ Steam returned an HTTP error."
        )

    except httpx.RequestError:
        await update.message.reply_text(
            "⚠️ Couldn't reach Steam right now."
        )

    except Exception as e:
        await update.message.reply_text(
            f"⚠️ Error while checking Steam: {e}"
        )
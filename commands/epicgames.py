import httpx
from telegram import Update
from telegram.ext import ContextTypes
from . import command

EPIC_URL = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions"

def extract_free_games(data):
    elements = data["data"]["Catalog"]["searchStore"]["elements"]
    free_games = []

    for game in elements:
        offers = (game.get("promotions") or {}).get("promotionalOffers", [])
        if not offers:
            continue  # not currently free, skip (could be upcoming instead)

        slug = game.get("productSlug")
        if not slug and game.get("offerMappings"):
            slug = game["offerMappings"][0].get("pageSlug")

        url = f"https://store.epicgames.com/en-US/p/{slug}" if slug else "https://store.epicgames.com/en-US/free-games"
        free_games.append({"title": game["title"], "url": url})

    return free_games

async def fetch_free_games():
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(EPIC_URL)
        resp.raise_for_status()
    return extract_free_games(resp.json())

@command("epicgames")
async def epicgames(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        games = await fetch_free_games()
        if not games:
            await update.message.reply_text("No free games listed right now — check back later.")
            return

        lines = ["🎮 Currently free on Epic Games:"]
        for g in games:
            lines.append(f"• {g['title']}\n  {g['url']}")
        await update.message.reply_text("\n".join(lines))

    except httpx.HTTPStatusError:
        await update.message.reply_text("⚠️ Epic Games API returned an error.")
    except (KeyError, ValueError, IndexError):
        await update.message.reply_text("⚠️ Got a response but couldn't parse it — Epic may have changed their API shape.")
    except httpx.RequestError:
        await update.message.reply_text("⚠️ Couldn't reach Epic Games right now.")
import httpx
from telegram import Update
from telegram.ext import ContextTypes
from users import save_user
from notify import notify_admin
from . import command

EPIC_URL = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions"


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


async def fetch_free_games():
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(EPIC_URL)
        resp.raise_for_status()

    return extract_free_games(resp.json())


@command("epicgames")
async def epicgames(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_new = save_user(update.effective_user)
    await notify_admin(context, update.effective_user, "/epicgames", is_new)

    try:
        games = await fetch_free_games()

        if not games:
            await update.message.reply_text(
                "🎮 No free Epic Games available right now."
            )
            return

        lines = [
            "🎮 *Epic Games Free Games*",
            "",
            f"🎁 *{len(games)} game(s) currently free:*",
            ""
        ]

        for i, game in enumerate(games, 1):
            lines.append(
                f"*{i}. {game['title']}*\n"
                f"🔗 {game['url']}\n"
            )

        lines.append("🎉 *Happy Gaming!*")

        await update.message.reply_text(
            "\n".join(lines),
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

    except httpx.HTTPStatusError:
        await update.message.reply_text(
            "⚠️ Epic Games API returned an error."
        )

    except httpx.RequestError:
        await update.message.reply_text(
            "⚠️ Couldn't reach Epic Games."
        )

    except Exception as e:
        await update.message.reply_text(
            f"⚠️ Error: {e}"
        )
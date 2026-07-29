import httpx
from telegram import Update
from telegram.ext import ContextTypes
from . import command

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

@command("btcprice")
async def btcprice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    params = {"ids": "bitcoin", "vs_currencies": "usd", "include_24hr_change": "true"}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(COINGECKO_URL, params=params)
            resp.raise_for_status()
        data = resp.json()["bitcoin"]
        price = data["usd"]
        change = data["usd_24h_change"]
        direction = "📈" if change >= 0 else "📉"

        await update.message.reply_text(
            f"Bitcoin: ${price:,.2f}\n"
            f"{direction} 24h change: {change:+.2f}%"
        )
    except httpx.HTTPStatusError:
        await update.message.reply_text("⚠️ CoinGecko returned an error.")
    except (KeyError, ValueError):
        await update.message.reply_text("⚠️ Got a response but couldn't parse it.")
    except httpx.RequestError:
        await update.message.reply_text("⚠️ Couldn't reach CoinGecko right now.")
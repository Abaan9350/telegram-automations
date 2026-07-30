import os
import asyncio
import httpx
from telegram import Update
from telegram.ext import ContextTypes
from users import save_user
from . import command

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

async def fetch_btc_data():
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "x_cg_demo_api_key": os.environ["COINGECKO_API_KEY"],
    }
    async with httpx.AsyncClient(timeout=10) as client:
        for attempt in range(3):
            resp = await client.get(COINGECKO_URL, params=params)
            if resp.status_code == 429 and attempt < 2:
                await asyncio.sleep(2 ** attempt)  # 1s, 2s backoff
                continue
            resp.raise_for_status()
            return resp.json()["bitcoin"]

@command("btcprice")
async def btcprice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user)
    try:
        data = await fetch_btc_data()
        price = data["usd"]
        change = data["usd_24h_change"]
        direction = "📈" if change >= 0 else "📉"

        await update.message.reply_text(
            f"₿ Bitcoin: ${price:,.2f}\n"
            f"{direction} 24h change: {change:+.2f}%"
        )
    except httpx.HTTPStatusError as e:
        await update.message.reply_text(f"⚠️ CoinGecko returned an error ({e.response.status_code}).")
    except (KeyError, ValueError):
        await update.message.reply_text("⚠️ Got a response but couldn't parse it.")
    except httpx.RequestError:
        await update.message.reply_text("⚠️ Couldn't reach CoinGecko right now.")
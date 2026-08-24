import datetime
import httpx
from telegram import Update
from telegram.ext import ContextTypes
from users import save_user
from notify import notify_admin
from . import command

NYT_URL = "https://www.nytimes.com/svc/wordle/v2/{date}.json"

@command("wordleanswer", "Get today's Wordle answer")
async def wordleanswer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_new = await save_user(update.effective_user)
    await notify_admin(context, update.effective_user, "/wordleanswer", is_new)
    today = datetime.date.today().isoformat()
    url = NYT_URL.format(date=today)

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
        solution = data["solution"].upper()
        await update.message.reply_text(f"🟩 Today's Wordle answer: {solution}")
    except httpx.HTTPStatusError:
        await update.message.reply_text("⚠️ NYT hasn't published today's answer yet.")
    except (KeyError, ValueError):
        await update.message.reply_text("⚠️ Got a response but couldn't parse it.")
    except httpx.RequestError:
        await update.message.reply_text("⚠️ Couldn't reach the NYT API right now.")
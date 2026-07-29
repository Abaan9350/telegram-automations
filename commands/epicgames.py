from telegram import Update
from telegram.ext import ContextTypes

from . import command


@command("epicgames")
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Test successful!\n\nYour Render deployment is working correctly."
    )
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from commands import load_all, COMMAND_HANDLERS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_BASE_URL = os.environ["WEBHOOK_BASE_URL"]   # e.g. https://abaandonebot.onrender.com
WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]        # any random string you pick
PORT = int(os.environ.get("PORT", 10000))


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Exception while handling an update:", exc_info=context.error)

    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ Something broke handling that command. I've logged it — try again in a bit."
        )


def main():
    load_all()

    app = Application.builder().token(BOT_TOKEN).build()
    for name, handler_func, _ in COMMAND_HANDLERS:
        app.add_handler(CommandHandler(name, handler_func))

    app.add_error_handler(error_handler)

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,                             # obscure path so randoms can't POST fake updates
        webhook_url=f"{WEBHOOK_BASE_URL}/{BOT_TOKEN}",
        secret_token=WEBHOOK_SECRET,
    )


if __name__ == "__main__":
    main()
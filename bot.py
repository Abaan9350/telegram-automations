import os
import logging
from telegram.ext import Application, CommandHandler
from commands import load_all, COMMAND_HANDLERS

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_BASE_URL = os.environ["WEBHOOK_BASE_URL"]   # e.g. https://abaandonebot.onrender.com
WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]        # any random string you pick
PORT = int(os.environ.get("PORT", 10000))

def main():
    load_all()

    app = Application.builder().token(BOT_TOKEN).build()
    for name, handler_func in COMMAND_HANDLERS:
        app.add_handler(CommandHandler(name, handler_func))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,                             # obscure path so randoms can't POST fake updates
        webhook_url=f"{WEBHOOK_BASE_URL}/{BOT_TOKEN}",
        secret_token=WEBHOOK_SECRET,
    )

if __name__ == "__main__":
    main()
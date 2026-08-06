import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from commands import load_all, COMMAND_HANDLERS

# Load environment variables from .env when running locally
load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
PORT = int(os.getenv("PORT", 10000))


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.exception("Exception while handling an update:", exc_info=context.error)

    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ Something went wrong while handling that command."
        )


async def prepare_polling(app: Application):
    """
    Remove webhook so Telegram starts sending updates via polling.
    Safe to call every time.
    """
    try:
        await app.bot.delete_webhook(drop_pending_updates=True)
        logger.info("Webhook removed successfully.")
    except TelegramError as e:
        logger.warning(f"Couldn't remove webhook: {e}")


def main():
    load_all()

    app = Application.builder().token(BOT_TOKEN).build()

    # Register all commands
    for name, handler_func, _ in COMMAND_HANDLERS:
        app.add_handler(CommandHandler(name, handler_func))

    app.add_error_handler(error_handler)

    # Running on Render?
    if os.getenv("RENDER"):
        logger.info("Running in WEBHOOK mode.")

        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,
            webhook_url=f"{WEBHOOK_BASE_URL}/{BOT_TOKEN}",
            secret_token=WEBHOOK_SECRET,
        )

    # Running locally
    else:
        logger.info("Running in POLLING mode.")

        app.post_init = prepare_polling

        app.run_polling(
            drop_pending_updates=True
        )


if __name__ == "__main__":
    main()
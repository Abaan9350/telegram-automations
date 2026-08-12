import os
import logging
import asyncio

import uvicorn
from http import HTTPStatus
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route
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


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    logger.exception(
        "Exception while handling an update:",
        exc_info=context.error,
    )

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


async def run_server(app: Application):
    """
    Run Telegram webhook and health endpoint on the same web server.
    """

    async def telegram_webhook(request: Request):
        # Verify Telegram's secret token
        if WEBHOOK_SECRET:
            received_secret = request.headers.get(
                "X-Telegram-Bot-Api-Secret-Token"
            )

            if received_secret != WEBHOOK_SECRET:
                return PlainTextResponse(
                    "Unauthorized",
                    status_code=HTTPStatus.UNAUTHORIZED,
                )

        data = await request.json()

        update = Update.de_json(
            data=data,
            bot=app.bot,
        )

        await app.update_queue.put(update)

        return PlainTextResponse("OK")


    async def health(request: Request):
        return PlainTextResponse(
            "OK",
            status_code=HTTPStatus.OK,
        )


    web_app = Starlette(
        routes=[
            Route(
                f"/{BOT_TOKEN}",
                telegram_webhook,
                methods=["POST"],
            ),
            Route(
                "/health",
                health,
                methods=["GET", "HEAD"],
            ),
        ]
    )


    await app.bot.set_webhook(
        url=f"{WEBHOOK_BASE_URL}/{BOT_TOKEN}",
        secret_token=WEBHOOK_SECRET,
        allowed_updates=Update.ALL_TYPES,
    )

    logger.info(
        f"Webhook set to: {WEBHOOK_BASE_URL}/{BOT_TOKEN}"
    )

    server = uvicorn.Server(
        uvicorn.Config(
            app=web_app,
            host="0.0.0.0",
            port=PORT,
            log_level="info",
        )
    )

    async with app:
        await app.start()
        await server.serve()
        await app.stop()


def main():
    load_all()

    # Render uses custom webhook server.
    # Local machine uses normal polling.
    if os.getenv("RENDER"):
        logger.info("Running in WEBHOOK mode.")

        app = (
            Application.builder()
            .token(BOT_TOKEN)
            .updater(None)
            .build()
        )

    else:
        logger.info("Running in POLLING mode.")

        app = (
            Application.builder()
            .token(BOT_TOKEN)
            .build()
        )

    # Register all commands
    for name, handler_func, _ in COMMAND_HANDLERS:
        app.add_handler(
            CommandHandler(name, handler_func)
        )

    app.add_error_handler(error_handler)

    if os.getenv("RENDER"):
        asyncio.run(run_server(app))

    else:
        app.post_init = prepare_polling

        app.run_polling(
            drop_pending_updates=True
        )


if __name__ == "__main__":
    main()
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from datetime import date
import requests
import os

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = date.today().strftime("%Y-%m-%d")

    wordle_url = f"https://www.nytimes.com/svc/wordle/v2/{today}.json"
    wordle = requests.get(wordle_url).json()

    answer = wordle["solution"].upper()

    await update.message.reply_text(
        f"🟩 Today's Wordle answer: {answer}"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("wordleanswer", start))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
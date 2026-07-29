# Telegram Automations Bot 🤖

A modular Telegram bot built using **Python** and **python-telegram-bot**.

The goal of this project is to create a personal automation bot where every new feature can be added as a separate command without modifying the core bot logic.

Currently deployed using **Render Webhooks**.

---

## ✨ Features

- Modular command system
- Automatic command discovery
- Telegram webhook deployment
- Easy-to-add new automations
- Async API requests using HTTPX

Current commands:

| Command | Description |
|---------|-------------|
| `/wordleanswer` | Get today's Wordle answer |
| `/test` | Test bot deployment status |

More commands will be added over time.

---

# 🏗️ Architecture

The project uses an auto-registration system.

Every command lives inside the `commands/` folder.

```
telegram-automations/

├── bot.py                  # Main bot entry point
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment configuration
│
├── commands/
│   ├── __init__.py         # Command registry
│   ├── wordleanswer.py     # Wordle command
│   └── test.py             # Test command
│
└── .env.example            # Environment variable template
```

---

# 🚀 Setup Locally

## 1. Clone the repository

```bash
git clone https://github.com/Abaan9350/telegram-automations.git

cd telegram-automations
```

---

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure environment variables

Create a `.env` file:

```env
BOT_TOKEN=your_bot_token_from_botfather

WEBHOOK_BASE_URL=https://your-app.onrender.com

WEBHOOK_SECRET=your_random_secret
```

Get your bot token from:

```
@BotFather
```

---

## 4. Run the bot

```bash
python bot.py
```

---

# ☁️ Deployment

This project uses Render Web Service with Telegram webhooks.

Deployment flow:

```
GitHub
   |
   |
Render
   |
   |
Telegram Webhook
   |
   |
Telegram Bot
```

## Render Setup

1. Create a new Web Service on Render.
2. Connect this GitHub repository.
3. Configure:

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
python bot.py
```

4. Add environment variables:

```
BOT_TOKEN
WEBHOOK_BASE_URL
WEBHOOK_SECRET
```

5. Deploy.

The bot automatically registers the Telegram webhook on startup.

---

# ➕ Adding a New Command

Adding commands is simple.

Create a new file inside:

```
commands/
```

Example:

```
commands/hello.py
```

Add:

```python
from telegram import Update
from telegram.ext import ContextTypes

from . import command


@command("hello")
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello from Telegram Automations!"
    )
```

That's it.

No changes are required in `bot.py`.

The command will automatically be detected after deployment.

---

# 🧠 How It Works

The command registry uses a decorator system.

Example:

```python
@command("hello")
async def hello(update, context):
    pass
```

When the bot starts:

1. It scans the `commands/` folder.
2. Imports every command file.
3. Registers all decorated functions.
4. Adds them as Telegram command handlers.

---

# 🛠️ Tech Stack

- Python 3
- python-telegram-bot
- HTTPX
- Render
- Telegram Bot API

---

# 📌 Future Commands

Planned automations:

- Epic Games free games
- Football updates
- Weather
- News
- Reddit feeds
- Stock/crypto alerts
- Personal productivity tools

---

# 📄 License

This project is licensed under the MIT License.

Feel free to fork, modify, and build your own automations.
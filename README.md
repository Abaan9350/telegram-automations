# Telegram Automations Bot 🤖

A personal Telegram automation bot built using **Python** and the **Telegram Bot API**.

This project is designed to provide useful automations and tools directly inside Telegram, such as commands, notifications, and API-powered features.

New automations can be added over time as the project grows.

---

# ✨ Features

- Telegram bot integration
- Custom commands
- Automated notifications
- API integrations
- Easy extension with new features
- Asynchronous request handling

---

# 📌 Available Features

Current features include:

- Wordle answer lookup
- Bot status testing
- Bitcoin price movement alerts

More automations will be added in the future.

---

# 🚀 Getting Started

## Prerequisites

Before running the project, make sure you have:

- Python 3.10 or higher
- A Telegram account
- A Telegram bot created using [BotFather](https://t.me/BotFather)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Abaan9350/telegram-automations.git
```

Navigate into the project:

```bash
cd telegram-automations
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ⚙️ Configuration

Create a `.env` file in the project directory:

```env
BOT_TOKEN=your_telegram_bot_token
WEBHOOK_BASE_URL=your_deployment_url
WEBHOOK_SECRET=your_webhook_secret
```

You can get your Telegram bot token from [BotFather](https://t.me/BotFather).

Never share your bot token publicly.

---

# ▶️ Running Locally

Start the bot using:

```bash
python bot.py
```

---

# ☁️ Deployment

The bot can be deployed using cloud platforms that support Python applications.

Deployment requires:

- Installing dependencies from `requirements.txt`
- Setting required environment variables
- Starting the bot application

---

# 🔐 Security

Do not commit sensitive information such as:

- Telegram bot tokens
- API keys
- Passwords
- `.env` files
- Private credentials

Use environment variables or secret managers to store sensitive data.

---

# 🧩 Adding New Features

The project is designed to be extended easily.

New functionality can be added by:

1. Creating a new module for the feature.
2. Connecting it with the Telegram bot.
3. Adding required configuration or API keys.
4. Testing locally before deployment.

---

# 🛠️ Tech Stack

- Python
- python-telegram-bot
- Telegram Bot API
- HTTPX
- GitHub Actions
- Render

---

# 📌 Future Plans

Possible future additions:

- More useful Telegram commands
- Additional price alerts
- Sports updates
- Weather notifications
- News summaries
- Personal productivity tools
- More API-based automations.

---

# 📄 License

This project is licensed under the MIT License.

Feel free to fork, modify, and build your own Telegram automations.

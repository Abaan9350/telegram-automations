# Telegram Automations 🤖

> A personal automation hub powered by Telegram.

Telegram Automations is a Python-based project that brings useful utilities, scheduled automations, and real-time notifications directly into Telegram.

The project is designed to be modular and easy to extend. New commands, integrations, and automations can be added without affecting the existing codebase.

---

## ✨ Highlights

* 🤖 Telegram Bot API integration
* ⚡ Modular command system
* 🔔 Scheduled automated notifications
* 🌐 External API integrations
* ☁️ Cloud deployment with Render
* ⏰ Scheduled workflows using GitHub Actions
* 🧩 Easily extensible architecture

---

## 📋 Current Commands

| Command         | Description                                           |
| --------------- | ----------------------------------------------------- |
| `/btcprice`     | Displays the current Bitcoin price and 24-hour change |
| `/epicgames`    | Lists the current free Epic Games Store games         |
| `/wordleanswer` | Shows today's Wordle answer                           |
| `/users`        | Displays registered bot users                         |

---

## 🔔 Current Automations

| Automation               | Description                                                                           |
| ------------------------ | ------------------------------------------------------------------------------------- |
| Bitcoin Price Alerts     | Sends an alert when Bitcoin's 24-hour price movement crosses the configured threshold |
| Epic Games Notifications | Automatically notifies when new free Epic Games become available                      |

---

## 🛠️ Tech Stack

* Python 3.12
* python-telegram-bot
* HTTPX
* Telegram Bot API
* CoinGecko API
* GitHub Actions
* Render

---

## 📂 Project Structure

```text
telegram-automations/
│
├── .github/
│   └── workflows/
│       ├── btc-alert.yml
│       └── epic-alert.yml
│
├── commands/
│   ├── btcprice.py
│   ├── epicgames.py
│   ├── expense.py
│   ├── users.py
│   ├── wordleanswer.py
│   └── __init__.py
│
├── scripts/
│   ├── btc_alert.py
│   └── epic_alert.py
│
├── services/
│   ├── google_sheets.py
│   └── __init__.py
│
├── state/
│   ├── btc_alert_state.json
│   └── epic_alert_state.json
│
├── .env.example
├── bot.py
├── config.py
├── notify.py
├── render.yaml
├── requirements.txt
├── users.py
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Before running the project, ensure you have:

* Python 3.10 or later (Python 3.12 recommended)
* A Telegram account
* A Telegram bot created using BotFather
* Git

---

## 📥 Installation

Clone the repository:

```bash
git clone https://github.com/Abaan9350/telegram-automations.git
```

Navigate to the project directory:

```bash
cd telegram-automations
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Create a `.env` file in the project root.

```env
BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
COINGECKO_API_KEY=your_coingecko_api_key
WEBHOOK_BASE_URL=your_render_url
WEBHOOK_SECRET=your_webhook_secret
```

> Never commit your `.env` file or API keys to GitHub.

---

## ▶️ Running Locally

Start the Telegram bot:

```bash
python bot.py
```

Run an automation manually:

```bash
python scripts/btc_alert.py
```

---

## ☁️ Deployment

The project is designed to run in the cloud.

### Telegram Bot

Hosted on **Render** for continuous availability.

### Scheduled Automations

Executed automatically using **GitHub Actions**.

Deployment requires:

* Installing dependencies from `requirements.txt`
* Configuring environment variables
* Deploying the bot
* Enabling GitHub Actions

---

## 🔐 Security

Sensitive information should **never** be committed to the repository.

Examples include:

* Telegram Bot Token
* API Keys
* Passwords
* Private Credentials
* `.env` files

Always use environment variables or secret managers.

---

## 🧩 Adding New Features

The project follows a modular structure.

To add a new feature:

1. Create a command or automation script.
2. Add any required service modules.
3. Configure API keys if needed.
4. Test locally.
5. Deploy and verify.

---

## 🚧 Roadmap

### Completed

* [x] Telegram Bot
* [x] Bitcoin Price Command
* [x] Bitcoin Price Alerts
* [x] Epic Games Command
* [x] Epic Games Notifications
* [x] Wordle Answer Command
* [x] User Management
* [x] Google Sheets service structure

### In Progress

* [ ] Supabase state storage
* [ ] Shared Telegram service
* [ ] Shared CoinGecko service
* [ ] Improved logging
* [ ] Better error handling

### Planned

* [ ] Expense tracker
* [ ] Weather updates
* [ ] Sports notifications
* [ ] News summaries
* [ ] AI assistant
* [ ] Home automation integration
* [ ] Raspberry Pi deployment
* [ ] Docker support

---

## 🤝 Contributing

This project is currently maintained as a personal automation platform, but suggestions and improvements are always welcome.

Feel free to fork the repository, experiment with new automations, and submit pull requests.

---

## 📄 License

This project is licensed under the **MIT License**.

Feel free to use, modify, and build upon it for your own automation projects.

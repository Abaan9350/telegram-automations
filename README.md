# Telegram Automations 🤖

> A personal automation hub powered by Telegram.

Telegram Automations is a Python-based personal automation platform that brings useful utilities, productivity tools, notifications, and finance tracking directly into Telegram.

The project is designed to be modular and easy to extend. New commands, integrations, and automations can be added without affecting the existing system.

---

## ✨ Highlights

- 🤖 Telegram Bot API integration
- ⚡ Modular command-based architecture
- 💰 Personal expense and income tracking
- 📊 Google Sheets integration
- 🔔 Automated notifications and alerts
- 🌐 External API integrations
- ☁️ Cloud deployment with Render
- ⏰ Scheduled workflows using GitHub Actions
- 🧩 Easily extensible architecture
- 🔐 Environment-based configuration

---

## 📋 Current Commands

| Command         | Description                                           |
| --------------- | ----------------------------------------------------- |
| `/btcprice`     | Displays the current Bitcoin price and 24-hour change |
| `/epicgames`    | Lists the current free Epic Games Store games         |
| `/wordleanswer` | Shows today's Wordle answer                           |
| `/expense`      | Records and processes personal expenses and income    |
| `/users`        | Displays registered bot users                         |

---

## 💰 Expense Tracker

The Telegram Expense Tracker allows expenses and income to be recorded directly through Telegram.

Example:

```text
Spent 250 on groceries
````

The system processes the message, identifies the transaction details, and stores the structured information in a Google Sheets budget tracker.

### Features

* 💸 Record expenses through Telegram
* 💰 Record income
* 🤖 Natural language transaction input
* 📊 Google Sheets storage
* 📅 Automatic date handling
* 🧾 Transaction descriptions
* 🔄 Easy access through Telegram

The goal is to make expense tracking as simple as sending a message.

---

## 🔔 Current Automations

| Automation               | Description                                                                           |
| ------------------------ | ------------------------------------------------------------------------------------- |
| Bitcoin Price Alerts     | Sends an alert when Bitcoin's 24-hour price movement crosses the configured threshold |
| Epic Games Notifications | Automatically notifies when new free Epic Games become available                      |
| Expense Tracker          | Processes Telegram messages and stores financial transactions in Google Sheets        |

---

## 🛠️ Tech Stack

* Python 3.12
* python-telegram-bot
* HTTPX
* Telegram Bot API
* Google Sheets API
* CoinGecko API
* GitHub Actions
* Render
* UptimeRobot

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

* Python 3.10 or later
* Python 3.12 recommended
* A Telegram account
* A Telegram bot created using BotFather
* Git
* Google Cloud credentials if using the Expense Tracker

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

For Google Sheets integration, configure the required Google credentials according to the project's service configuration.

> Never commit your `.env` file, API keys, or private credentials to GitHub.

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

The project is designed to run continuously in the cloud.

### Telegram Bot

The Telegram bot is hosted on **Render**.

Render provides the cloud environment required to keep the bot available without running it manually on a local computer.

### Keeping the Service Active

An uptime monitoring service can periodically ping the deployed application to help prevent the free hosting service from becoming inactive.

### Scheduled Automations

Scheduled tasks such as Bitcoin alerts and Epic Games notifications can be executed using **GitHub Actions**.

Deployment requires:

* Installing dependencies from `requirements.txt`
* Configuring environment variables
* Deploying the application to Render
* Configuring GitHub Actions
* Configuring required external API credentials

---

## 🔐 Security

Sensitive information should **never** be committed to the repository.

Examples include:

* Telegram Bot Token
* API Keys
* Google credentials
* Passwords
* Private credentials
* `.env` files

Always use environment variables, GitHub Secrets, or appropriate secret management solutions.

---

## 🧩 Architecture

The project separates different responsibilities into individual modules.

```text
                    ┌──────────────────┐
                    │     Telegram     │
                    │      User        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Telegram Bot    │
                    │     bot.py       │
                    └────────┬─────────┘
                             │
             ┌───────────────┼───────────────┐
             ▼               ▼               ▼
       ┌───────────┐   ┌────────────┐  ┌────────────┐
       │ Commands  │   │  Services  │  │Automations │
       └─────┬─────┘   └──────┬─────┘  └──────┬─────┘
             │                │               │
             ▼                ▼               ▼
       Telegram         Google Sheets    GitHub Actions
       Utilities        External APIs    Scheduled Tasks
```

This structure makes it easier to add new commands and integrations without modifying the entire application.

---

## 🧩 Adding New Features

The project follows a modular structure.

To add a new feature:

1. Create a command or automation script.
2. Add any required service modules.
3. Configure API keys or credentials if required.
4. Register the command with the Telegram bot.
5. Test locally.
6. Deploy and verify.

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
* [x] Google Sheets Integration
* [x] Telegram Expense Tracker
* [x] Cloud Deployment with Render

### In Progress

* [ ] Supabase state storage
* [ ] Shared Telegram service
* [ ] Shared CoinGecko service
* [ ] Improved logging
* [ ] Better error handling
* [ ] Improved expense categorization

### Planned

* [ ] Weather updates
* [ ] Sports notifications
* [ ] News summaries
* [ ] AI assistant
* [ ] More personal productivity tools
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

```
```

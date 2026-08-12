<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Abaan9350/telegram-automations">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Telegram Automations 🤖</h3>

  <p align="center">
    A personal automation hub powered by Telegram.
    <br />
    Automate everyday tasks, track expenses, receive notifications, and build useful utilities directly through Telegram.
    <br />
    <br />
    <a href="https://github.com/Abaan9350/telegram-automations">View Repository</a>
    &middot;
    <a href="https://github.com/Abaan9350/telegram-automations/issues">Report Bug</a>
    &middot;
    <a href="https://github.com/Abaan9350/telegram-automations/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#current-features">Current Features</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Telegram Automations is a personal Python-based automation platform built around the Telegram Bot API.

The goal of the project is simple: instead of opening different applications or manually repeating everyday tasks, useful tools and automations can be accessed directly through Telegram.

The project is designed with a modular architecture so that new commands, services, APIs, and automations can be added without affecting the existing functionality.

### Current Features

- 🤖 Telegram Bot integration
- 💰 Personal expense and income tracking
- 📊 Google Sheets integration
- ₿ Bitcoin price tracking
- 🔔 Bitcoin price alerts
- 🎮 Epic Games free game notifications
- 🟩 Wordle answer utility
- 👥 Telegram user management
- ☁️ Render cloud deployment
- ⏰ GitHub Actions scheduled workflows
- 🌐 External API integrations
- 🧩 Modular command structure

### Expense Tracker

One of the main features of the project is a personal finance tracker that works entirely through Telegram.

Users can send natural language messages such as:

```text
Spent 250 on groceries
````

The system processes the message and records the relevant transaction information in Google Sheets.

This makes tracking daily expenses much faster than manually opening a spreadsheet or finance application.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CURRENT FEATURES -->

## Current Features

### Telegram Commands

| Command         | Description                                           |
| --------------- | ----------------------------------------------------- |
| `/btcprice`     | Displays the current Bitcoin price and 24-hour change |
| `/epicgames`    | Lists the current free Epic Games Store games         |
| `/wordleanswer` | Shows today's Wordle answer                           |
| `/expense`      | Records and processes personal expenses and income    |
| `/users`        | Displays registered bot users                         |

### Automated Notifications

| Automation               | Description                                                                           |
| ------------------------ | ------------------------------------------------------------------------------------- |
| Bitcoin Price Alerts     | Sends an alert when Bitcoin's 24-hour price movement crosses the configured threshold |
| Epic Games Notifications | Automatically notifies when new free Epic Games become available                      |
| Expense Tracker          | Processes Telegram messages and stores financial transactions in Google Sheets        |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- BUILT WITH -->

### Built With

* [![Python][Python-badge]][Python-url]
* [![Telegram][Telegram-badge]][Telegram-url]
* [![Google Sheets][GoogleSheets-badge]][GoogleSheets-url]
* [![GitHub Actions][GitHubActions-badge]][GitHubActions-url]
* [![Render][Render-badge]][Render-url]

Additional libraries and services used by the project include:

* Python 3.12
* python-telegram-bot
* HTTPX
* CoinGecko API
* Google Sheets API
* UptimeRobot

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy of the project up and running, follow these steps.

### Prerequisites

Before running the project, make sure you have:

* Python 3.10 or later
* Python 3.12 recommended
* A Telegram account
* A Telegram bot created using BotFather
* Git
* Google Cloud credentials if using the Expense Tracker

### Installation

1. Clone the repository

   ```sh
   git clone https://github.com/Abaan9350/telegram-automations.git
   ```

2. Navigate to the project directory

   ```sh
   cd telegram-automations
   ```

3. Install the required packages

   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root

   ```env
   BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   COINGECKO_API_KEY=your_coingecko_api_key
   WEBHOOK_BASE_URL=your_render_url
   WEBHOOK_SECRET=your_webhook_secret
   ```

5. Configure Google Sheets credentials if you are using the Expense Tracker.

> Never commit your `.env` file, API keys, or private credentials to GitHub.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

Once the bot is running, commands can be sent directly through Telegram.

### Bitcoin Price

```text
/btcprice
```

Returns the current Bitcoin price along with its 24-hour price movement.

### Epic Games

```text
/epicgames
```

Returns the currently available free games on the Epic Games Store.

### Wordle

```text
/wordleanswer
```

Returns the current Wordle answer.

### Expense Tracker

Natural language messages can be used to record transactions.

Example:

```text
Spent 250 on groceries
```

The transaction is processed and stored in the connected Google Sheets budget tracker.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- PROJECT STRUCTURE -->

## Project Structure

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

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- DEPLOYMENT -->

## Deployment

The project is designed to run in the cloud.

### Render

The Telegram bot is hosted on Render for continuous availability.

### GitHub Actions

Scheduled automations such as Bitcoin price alerts and Epic Games notifications are executed using GitHub Actions.

### Uptime Monitoring

UptimeRobot can be used to periodically ping the deployed service to help prevent the Render free service from becoming inactive.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- SECURITY -->

## Security

Sensitive information should never be committed to the repository.

Examples include:

* Telegram Bot Token
* API Keys
* Google credentials
* Passwords
* Private credentials
* `.env` files

Use environment variables and GitHub Secrets wherever appropriate.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

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
* [x] Render Deployment

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

See the [open issues](https://github.com/Abaan9350/telegram-automations/issues) for a full list of proposed features and improvements.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

This is currently a personal automation platform, but suggestions and improvements are always welcome.

If you have an idea for a new automation or feature, feel free to open an issue or fork the project and experiment with it.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Abdurrahman - [@Abaan9350](https://github.com/Abaan9350) - [abaan9350@gmail.com](mailto:abaan9350@gmail.com)

Project Link: [https://github.com/Abaan9350/telegram-automations](https://github.com/Abaan9350/telegram-automations)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/Abaan9350/telegram-automations.svg?style=for-the-badge
[contributors-url]: https://github.com/Abaan9350/telegram-automations/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Abaan9350/telegram-automations.svg?style=for-the-badge
[forks-url]: https://github.com/Abaan9350/telegram-automations/network/members
[stars-shield]: https://img.shields.io/github/stars/Abaan9350/telegram-automations.svg?style=for-the-badge
[stars-url]: https://github.com/Abaan9350/telegram-automations/stargazers
[issues-shield]: https://img.shields.io/github/issues/Abaan9350/telegram-automations.svg?style=for-the-badge
[issues-url]: https://github.com/Abaan9350/telegram-automations/issues
[license-shield]: https://img.shields.io/github/license/Abaan9350/telegram-automations.svg?style=for-the-badge
[license-url]: https://github.com/Abaan9350/telegram-automations/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/
[Python-badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Telegram-badge]: https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white
[Telegram-url]: https://telegram.org/
[GoogleSheets-badge]: https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=googlesheets&logoColor=white
[GoogleSheets-url]: https://www.google.com/sheets/about/
[GitHubActions-badge]: https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white
[GitHubActions-url]: https://github.com/features/actions
[Render-badge]: https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white
[Render-url]: https://render.com/

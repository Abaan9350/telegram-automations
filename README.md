<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][https://www.linkedin.com/in/abaan9350/]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Abaan9350/telegram-automations">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Telegram Automations 🤖</h3>

  <p align="center">
    A personal automation hub powered by Telegram and AI.
    <br />
    Discover historical events, monitor crypto, get free game alerts, and more—all through Telegram.
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
        <li><a href="#key-features">Key Features</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#configuration">Configuration</a></li>
      </ul>
    </li>
    <li><a href="#features">Features</a>
      <ul>
        <li><a href="#telegram-commands">Telegram Commands</a></li>
        <li><a href="#automated-alerts">Automated Alerts</a></li>
      </ul>
    </li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li><a href="#deployment">Deployment</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Telegram Automations is a personal Python-based automation platform built around the Telegram Bot API and powered by Google Gemini AI.

The goal is simple: instead of opening different applications or manually repeating everyday tasks, access useful tools and automations directly through Telegram—from tracking expenses to discovering fascinating historical events curated by AI.

The project follows a modular architecture, making it easy to add new commands, services, and automations without affecting existing functionality.

### Key Features

- 🤖 **Telegram Bot** - Natural language interface for all automations
- 🧠 **AI-Powered Content** - Google Gemini ranks and generates social media content
- 📅 **Historical Events** - Discover interesting events from "this day in history"
- ₿ **Bitcoin Monitoring** - Real-time price tracking and automated alerts
- 🎮 **Free Game Alerts** - Automated notifications for Epic Games and Steam
- 🎬 **Multi-Source Events** - Sports, music, movies, TV, gaming, and Wikipedia
- ⏰ **GitHub Actions** - Scheduled workflows for automated monitoring
- ☁️ **Cloud Deployment** - Production-ready on Render
- 🧩 **Modular Architecture** - Easy to extend and customize

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- BUILT WITH -->

### Built With

* [![Python][Python-badge]][Python-url]
* [![Telegram][Telegram-badge]][Telegram-url]
* [![Google Gemini][Gemini-badge]][Gemini-url]
* [![GitHub Actions][GitHubActions-badge]][GitHubActions-url]
* [![Render][Render-badge]][Render-url]

**Core Technologies:**
* Python 3.12
* python-telegram-bot (async)
* Google Gemini API
* Starlette & Uvicorn (webhook server)
* HTTPX (async HTTP client)
* aiosqlite (async database)

**External APIs:**
* Wikipedia / Wikimedia REST API
* TheSportsDB
* MusicBrainz
* TMDB (The Movie Database)
* IGDB (Internet Game Database)
* CoinGecko API

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

Before running the project, ensure you have:

* **Python 3.10 or later** (Python 3.12 recommended)
* **A Telegram account**
* **A Telegram bot** created using [@BotFather](https://t.me/botfather)
* **Git**
* **API Keys** (depending on features you want to use):
  - Google Gemini API key (for `/today` command)
  - CoinGecko API key (for Bitcoin tracking)
  - TMDB API token (optional, for movies/TV)
  - IGDB credentials (optional, for gaming)

### Installation

1. **Clone the repository**

   ```sh
   git clone https://github.com/Abaan9350/telegram-automations.git
   cd telegram-automations
   ```

2. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Copy the example file and configure your credentials:

   ```sh
   cp .env.example .env
   ```

   Edit `.env` with your actual values. See [Configuration](#configuration) for details.

4. **Run the bot**

   For local development (polling mode):

   ```sh
   python bot.py
   ```

   For production (webhook mode), set `RENDER=true` in your `.env` file.

> ⚠️ **Security Warning**: Never commit your `.env` file, API keys, or private credentials to GitHub.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Configuration

The project uses environment variables for configuration. See `.env.example` for a complete list of available options.

#### Required Variables

```env
# Core bot configuration
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_ID=your_telegram_user_id
```

#### Optional Variables (by feature)

**For `/today` command:**
```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
SPORTSDB_API_KEY=123
TMDB_API_TOKEN=your_tmdb_token
IGDB_CLIENT_ID=your_igdb_client_id
IGDB_CLIENT_SECRET=your_igdb_client_secret
TIMEZONE=Asia/Kolkata
```

**For Bitcoin tracking:**
```env
COINGECKO_API_KEY=your_coingecko_api_key
TELEGRAM_CHAT_ID=your_chat_id
```

**For free game alerts:**
```env
EPIC_GAMES_CHAT_IDS=123456789,987654321
STEAM_GAMES_CHAT_IDS=123456789,987654321
```

**For production deployment:**
```env
WEBHOOK_BASE_URL=https://your-app.onrender.com
WEBHOOK_SECRET=your_random_secret
PORT=10000
RENDER=true
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FEATURES -->

## Features

### Telegram Commands

| Command         | Description                                                                 |
| --------------- | --------------------------------------------------------------------------- |
| `/today`        | 🔥 Discover interesting historical events from "this day in history"       |
| `/btcprice`     | ₿ Get current Bitcoin price and 24-hour percentage change                  |
| `/epicgames`    | 🎮 List currently free games on Epic Games Store                           |
| `/steamgames`   | 🎮 List currently free games on Steam                                      |
| `/wordleanswer` | 🟩 Get today's Wordle answer                                               |
| `/users`        | 👥 Display registered bot users (admin only)                               |

### `/today` - AI-Powered Historical Events

The flagship feature of this bot. Powered by Google Gemini AI, it discovers and ranks fascinating historical events.

**How it works:**

1. **Search** - Fetches events from multiple sources:
   - Wikipedia (general historical events)
   - TheSportsDB (sports history)
   - MusicBrainz (album releases)
   - TMDB (movie and TV premieres)
   - IGDB (video game releases)

2. **AI Ranking** - Gemini analyzes all candidates and selects the 3 most interesting events based on:
   - Social media potential
   - Category diversity (Sports, Music, Gaming, Technology, etc.)
   - Cultural significance
   - Storytelling value

3. **Content Generation** - For your selected event, Gemini generates:
   - A ready-to-post Twitter/X thread
   - A Reddit post with title, body, and suggested subreddit
   - Downloaded image from the source

4. **Social Media Ready** - Copy the generated content and post manually to your social media accounts.

**Example Usage:**

```
User: /today
Bot: 🔎 Searching today's historical events...
Bot: 🔎 Found 47 historical candidates.
     🧠 Gemini is choosing the three most interesting ones...
Bot: [Shows 3 top events with selection buttons]
User: [Selects event #2]
Bot: [Generates Twitter post, Reddit post, and downloads image]
```

### Automated Alerts

The bot includes GitHub Actions workflows that run on a schedule to monitor various services:

| Alert Type              | Schedule        | Description                                                     |
| ----------------------- | --------------- | --------------------------------------------------------------- |
| **Bitcoin Price**       | Every 6 hours   | Alert when BTC moves ±1% in 24 hours (configurable threshold)  |
| **Epic Games**          | Twice daily     | Notify when new free games are available                        |
| **Steam Games**         | Twice daily     | Notify when new free-to-keep games appear                       |

All alerts include:
- 24-hour cooldown to prevent spam
- State persistence between runs
- Manual workflow trigger for testing
- Configurable recipient lists

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- PROJECT STRUCTURE -->

## Project Structure

```text
telegram-automations/
│
├── .github/
│   └── workflows/              # GitHub Actions scheduled jobs
│       ├── btc-alert.yml       # Bitcoin price monitoring
│       ├── epic-alert.yml      # Epic Games monitoring
│       └── steam-alert.yml     # Steam games monitoring
│
├── commands/                   # Telegram bot commands
│   ├── __init__.py             # Command registry
│   ├── btcprice.py             # Bitcoin price command
│   ├── epicgames.py            # Epic Games command
│   ├── steamgames.py           # Steam games command
│   ├── today.py                # Historical events command
│   ├── users.py                # User management
│   └── wordleanswer.py         # Wordle answer
│
├── services/                   # Shared service modules
│   ├── __init__.py
│   ├── gemini.py               # Google Gemini AI integration
│   ├── historical_events.py    # Wikipedia API integration
│   ├── additional_sources.py   # Sports, music, movies, gaming APIs
│   ├── content_generator.py    # Social media content generation
│   └── media.py                # Image downloading
│
├── scripts/                    # GitHub Actions scripts
│   ├── config.py               # Shared configuration
│   ├── btc_alert.py            # Bitcoin alert script
│   ├── epic_alert.py           # Epic Games alert script
│   └── steam_alert.py          # Steam games alert script
│
├── state/                      # Alert state persistence
│   ├── btc_alert_state.json
│   ├── epic_alert_state.json
│   └── steam_alert_state.json
│
├── credentials/                # Service account credentials (gitignored)
│   └── google-service-account.json
│
├── .env.example                # Environment variable template
├── bot.py                      # Main bot entry point
├── notify.py                   # Admin notifications
├── users.py                    # User database management
├── users.db                    # SQLite user database
├── render.yaml                 # Render deployment config
├── requirements.txt            # Python dependencies
└── README.md
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- DEPLOYMENT -->

## Deployment

The project is designed for cloud deployment with minimal configuration.

### Render (Recommended)

The bot runs continuously on [Render](https://render.com/) using the included `render.yaml` configuration.

**Setup:**

1. Fork this repository
2. Connect your GitHub account to Render
3. Create a new Web Service from your fork
4. Add environment variables in the Render dashboard
5. Deploy

The bot automatically switches to webhook mode when `RENDER=true` is set.

### GitHub Actions

Scheduled alerts run via GitHub Actions workflows:

1. Add repository secrets:
   - `BOT_TOKEN`
   - `COINGECKO_API_KEY`
   - `TELEGRAM_CHAT_ID`
   - `EPIC_GAMES_CHAT_IDS`
   - `STEAM_GAMES_CHAT_IDS`

2. Enable GitHub Actions in your repository settings

3. Workflows run automatically on schedule:
   - Bitcoin: Every 6 hours
   - Epic Games: 6 AM & 6 PM UTC
   - Steam: 6 AM & 6 PM UTC

### Local Development

For testing, run in polling mode (no webhook required):

```sh
# Don't set RENDER variable
python bot.py
```

The bot polls Telegram's servers for updates instead of listening for webhooks.

### Uptime Monitoring

Optional: Use [UptimeRobot](https://uptimerobot.com/) to ping your `/health` endpoint and prevent Render's free tier from sleeping.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

### ✅ Completed

* [x] Telegram Bot with webhook and polling support
* [x] Bitcoin price tracking and alerts
* [x] Epic Games free game notifications
* [x] Steam free game notifications
* [x] Google Sheets expense tracker
* [x] User management system
* [x] **AI-powered historical events discovery** 🆕
* [x] **Multi-source event aggregation** (Wikipedia, Sports, Music, Movies, Gaming) 🆕
* [x] **Google Gemini integration for content generation** 🆕
* [x] **Social media post generation** (Twitter, Reddit) 🆕
* [x] Render cloud deployment
* [x] GitHub Actions automation
* [x] Async/await architecture
* [x] SQLite database for user tracking

### 🚧 In Progress

* [ ] Enhanced error handling and retry logic
* [ ] Improved logging and monitoring
* [ ] Unit and integration tests

### 📋 Planned

* [ ] Weather updates and forecasts
* [ ] News summaries with AI analysis
* [ ] More personal productivity tools
* [ ] Home automation integration (Home Assistant)
* [ ] Docker containerization
* [ ] Raspberry Pi deployment guide
* [ ] Web dashboard for analytics
* [ ] Multi-user support with permissions
* [ ] Database migration to PostgreSQL
* [ ] Automated social media posting (optional)

See the [open issues](https://github.com/Abaan9350/telegram-automations/issues) for a full list of proposed features and known issues.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

This is primarily a personal automation platform, but contributions, suggestions, and improvements are welcome!

If you have an idea for a new automation or feature:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

**Contribution Ideas:**
- New Telegram commands
- Additional data sources for `/today`
- New alert types
- Bug fixes and optimizations
- Documentation improvements

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

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

This project integrates with several excellent APIs and services:

* [Telegram Bot API](https://core.telegram.org/bots/api)
* [Google Gemini AI](https://ai.google.dev/)
* [Wikipedia / Wikimedia REST API](https://www.mediawiki.org/wiki/API:REST_API)
* [TheSportsDB](https://www.thesportsdb.com/)
* [MusicBrainz](https://musicbrainz.org/)
* [TMDB](https://www.themoviedb.org/)
* [IGDB](https://www.igdb.com/)
* [CoinGecko](https://www.coingecko.com/)
* [Epic Games Store](https://www.epicgames.com/store/)
* [Steam](https://store.steampowered.com/)

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
[linkedin-url]: https://www.linkedin.com/in/abaan9350/
[Python-badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Telegram-badge]: https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white
[Telegram-url]: https://telegram.org/
[Gemini-badge]: https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white
[Gemini-url]: https://ai.google.dev/
[GoogleSheets-badge]: https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=googlesheets&logoColor=white
[GoogleSheets-url]: https://www.google.com/sheets/about/
[GitHubActions-badge]: https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white
[GitHubActions-url]: https://github.com/features/actions
[Render-badge]: https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white
[Render-url]: https://render.com/

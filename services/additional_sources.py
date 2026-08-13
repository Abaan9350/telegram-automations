import asyncio
import os
import time
from datetime import date, datetime, timezone
from typing import Any

import httpx
from dotenv import load_dotenv


load_dotenv()


# ============================================================
# Common configuration
# ============================================================

TIMEOUT = 20

USER_AGENT = (
    "TelegramAutomations/1.0 "
    "(personal historical content project)"
)


# We search these historical milestones.
LOOKBACK_YEARS = [
    5,
    10,
    15,
    20,
    25,
    30,
]


# ============================================================
# TheSportsDB
# ============================================================

SPORTSDB_API_KEY = os.getenv(
    "SPORTSDB_API_KEY",
    "123",
)

SPORTSDB_URL = (
    "https://www.thesportsdb.com/api/v1/json/"
    f"{SPORTSDB_API_KEY}/eventsday.php"
)


async def fetch_sports_events(
    target_date: date,
) -> list[dict[str, Any]]:

    events = []

    async with httpx.AsyncClient(
        timeout=TIMEOUT,
        headers={
            "User-Agent": USER_AGENT,
        },
    ) as client:

        for years_ago in LOOKBACK_YEARS:

            historical_year = (
                target_date.year - years_ago
            )

            historical_date = date(
                historical_year,
                target_date.month,
                target_date.day,
            )

            try:

                results = await fetch_sports_day(
                    client=client,
                    historical_date=historical_date,
                    years_ago=years_ago,
                )

                events.extend(results)

            except Exception as e:

                print(
                    "Sports source error:",
                    e,
                )

            # Keep comfortably below the free
            # API's documented rate limit.
            await asyncio.sleep(0.5)

    return events


async def fetch_sports_day(
    client: httpx.AsyncClient,
    historical_date: date,
    years_ago: int,
) -> list[dict[str, Any]]:

    response = await client.get(
        SPORTSDB_URL,
        params={
            "d": historical_date.isoformat(),
        },
    )

    response.raise_for_status()

    data = response.json()

    raw_events = (
        data.get("events")
        or []
    )

    results = []

    for item in raw_events:

        title = (
            item.get("strEvent")
            or ""
        ).strip()

        if not title:
            continue

        sport = (
            item.get("strSport")
            or "Sports"
        ).strip()

        league = (
            item.get("strLeague")
            or ""
        ).strip()

        venue = (
            item.get("strVenue")
            or ""
        ).strip()

        home_team = (
            item.get("strHomeTeam")
            or ""
        ).strip()

        away_team = (
            item.get("strAwayTeam")
            or ""
        ).strip()

        home_score = item.get(
            "intHomeScore"
        )

        away_score = item.get(
            "intAwayScore"
        )

        score = ""

        if (
            home_score is not None
            and away_score is not None
        ):

            score = (
                f"{home_score}-{away_score}"
            )

        description_parts = []

        if sport:
            description_parts.append(
                f"Sport: {sport}"
            )

        if league:
            description_parts.append(
                f"Competition: {league}"
            )

        if home_team and away_team:
            description_parts.append(
                f"{home_team} vs {away_team}"
            )

        if score:
            description_parts.append(
                f"Score: {score}"
            )

        if venue:
            description_parts.append(
                f"Venue: {venue}"
            )

        description = " | ".join(
            description_parts
        )

        event_text = title

        if description:
            event_text += (
                f". {description}."
            )

        source_url = (
            "https://www.thesportsdb.com/"
        )

        image_url = (
            item.get("strThumb")
            or item.get("strPoster")
            or item.get(
                "strHomeTeamBadge"
            )
            or item.get(
                "strAwayTeamBadge"
            )
        )

        results.append(
            {
                "year": historical_date.year,
                "date": historical_date.isoformat(),
                "display_date": (
                    f"{historical_date.day} "
                    f"{historical_date.strftime('%B')} "
                    f"{historical_date.year}"
                ),
                "years_ago": years_ago,
                "source_category": "sports",
                "title": title,
                "event": event_text,
                "description": description,
                "extract": "",
                "source_url": source_url,
                "image_url": image_url,
            }
        )

    return results


# ============================================================
# MusicBrainz
# ============================================================

MUSICBRAINZ_URL = (
    "https://musicbrainz.org/ws/2/release/"
)

MUSICBRAINZ_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
}


async def fetch_music_events(
    target_date: date,
) -> list[dict[str, Any]]:

    events = []

    async with httpx.AsyncClient(
        timeout=TIMEOUT,
        headers=MUSICBRAINZ_HEADERS,
    ) as client:

        for years_ago in LOOKBACK_YEARS:

            historical_year = (
                target_date.year - years_ago
            )

            historical_date = date(
                historical_year,
                target_date.month,
                target_date.day,
            )

            try:

                results = await fetch_music_day(
                    client=client,
                    historical_date=historical_date,
                    years_ago=years_ago,
                )

                events.extend(results)

            except Exception as e:

                print(
                    "Music source error:",
                    e,
                )

            # MusicBrainz asks clients to
            # be considerate with request rate.
            await asyncio.sleep(1.1)

    return events


async def fetch_music_day(
    client: httpx.AsyncClient,
    historical_date: date,
    years_ago: int,
) -> list[dict[str, Any]]:

    query = (
        f"date:{historical_date.isoformat()}"
    )

    response = await client.get(
        MUSICBRAINZ_URL,
        params={
            "query": query,
            "fmt": "json",
            "limit": 20,
            "inc": "artist-credits+release-groups",
        },
    )

    response.raise_for_status()

    data = response.json()

    releases = (
        data.get("releases")
        or []
    )

    results = []

    for release in releases:

        title = (
            release.get("title")
            or ""
        ).strip()

        if not title:
            continue

        artist = extract_artist(
            release
        )

        release_id = (
            release.get("id")
            or ""
        )

        if artist:
            display_title = (
                f"{title} by {artist}"
            )
        else:
            display_title = title

        source_url = (
            f"https://musicbrainz.org/release/"
            f"{release_id}"
            if release_id
            else "https://musicbrainz.org/"
        )

        image_url = None

        if release_id:

            image_url = (
                "https://coverartarchive.org/"
                f"release/{release_id}/front-500"
            )

        event_text = (
            f"{display_title} was released "
            f"on {historical_date.day} "
            f"{historical_date.strftime('%B')} "
            f"{historical_date.year}."
        )

        results.append(
            {
                "year": historical_date.year,
                "date": historical_date.isoformat(),
                "display_date": (
                    f"{historical_date.day} "
                    f"{historical_date.strftime('%B')} "
                    f"{historical_date.year}"
                ),
                "years_ago": years_ago,
                "source_category": "music",
                "title": display_title,
                "event": event_text,
                "description": (
                    "Music release recorded by "
                    "MusicBrainz."
                ),
                "extract": "",
                "source_url": source_url,
                "image_url": image_url,
            }
        )

    return results


def extract_artist(
    release: dict,
) -> str:

    artist_credits = (
        release.get(
            "artist-credit"
        )
        or []
    )

    parts = []

    for credit in artist_credits:

        artist = (
            credit.get("artist")
            or {}
        )

        name = (
            artist.get("name")
            or ""
        ).strip()

        if name:
            parts.append(name)

        joinphrase = (
            credit.get("joinphrase")
            or ""
        )

        if joinphrase:
            parts.append(
                joinphrase
            )

    return "".join(
        parts
    ).strip()


# ============================================================
# TMDB
# ============================================================

TMDB_API_TOKEN = os.getenv(
    "TMDB_API_TOKEN"
)

TMDB_BASE_URL = (
    "https://api.themoviedb.org/3"
)


async def fetch_tmdb_events(
    target_date: date,
) -> list[dict[str, Any]]:

    if not TMDB_API_TOKEN:

        print(
            "TMDB_API_TOKEN not configured. "
            "Skipping movies and TV."
        )

        return []

    events = []

    headers = {
        "Authorization": (
            f"Bearer {TMDB_API_TOKEN}"
        ),
        "accept": "application/json",
        "User-Agent": USER_AGENT,
    }

    async with httpx.AsyncClient(
        timeout=TIMEOUT,
        headers=headers,
    ) as client:

        for years_ago in LOOKBACK_YEARS:

            historical_year = (
                target_date.year - years_ago
            )

            historical_date = date(
                historical_year,
                target_date.month,
                target_date.day,
            )

            try:

                movies = await fetch_tmdb_movies(
                    client,
                    historical_date,
                    years_ago,
                )

                events.extend(movies)

                tv = await fetch_tmdb_tv(
                    client,
                    historical_date,
                    years_ago,
                )

                events.extend(tv)

            except Exception as e:

                print(
                    "TMDB source error:",
                    e,
                )

    return events


async def fetch_tmdb_movies(
    client: httpx.AsyncClient,
    historical_date: date,
    years_ago: int,
) -> list[dict[str, Any]]:

    date_text = (
        historical_date.isoformat()
    )

    response = await client.get(
        f"{TMDB_BASE_URL}/discover/movie",
        params={
            "language": "en-US",
            "include_adult": "false",
            "include_video": "false",
            "primary_release_date.gte": date_text,
            "primary_release_date.lte": date_text,
            "sort_by": "popularity.desc",
            "page": 1,
        },
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for movie in (
        data.get("results")
        or []
    )[:15]:

        title = (
            movie.get("title")
            or ""
        ).strip()

        if not title:
            continue

        movie_id = movie.get(
            "id"
        )

        overview = (
            movie.get("overview")
            or ""
        ).strip()

        poster_path = (
            movie.get("poster_path")
        )

        image_url = None

        if poster_path:

            image_url = (
                "https://image.tmdb.org/t/p/"
                "w780"
                f"{poster_path}"
            )

        source_url = (
            f"https://www.themoviedb.org/movie/"
            f"{movie_id}"
            if movie_id
            else "https://www.themoviedb.org/"
        )

        event_text = (
            f"{title} had its primary release "
            f"on {historical_date.day} "
            f"{historical_date.strftime('%B')} "
            f"{historical_date.year}."
        )

        results.append(
            {
                "year": historical_date.year,
                "date": historical_date.isoformat(),
                "display_date": (
                    f"{historical_date.day} "
                    f"{historical_date.strftime('%B')} "
                    f"{historical_date.year}"
                ),
                "years_ago": years_ago,
                "source_category": "movies",
                "title": title,
                "event": event_text,
                "description": overview,
                "extract": "",
                "source_url": source_url,
                "image_url": image_url,
            }
        )

    return results


async def fetch_tmdb_tv(
    client: httpx.AsyncClient,
    historical_date: date,
    years_ago: int,
) -> list[dict[str, Any]]:

    date_text = (
        historical_date.isoformat()
    )

    response = await client.get(
        f"{TMDB_BASE_URL}/discover/tv",
        params={
            "language": "en-US",
            "first_air_date.gte": date_text,
            "first_air_date.lte": date_text,
            "sort_by": "popularity.desc",
            "page": 1,
        },
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for show in (
        data.get("results")
        or []
    )[:15]:

        title = (
            show.get("name")
            or ""
        ).strip()

        if not title:
            continue

        show_id = show.get(
            "id"
        )

        overview = (
            show.get("overview")
            or ""
        ).strip()

        poster_path = (
            show.get("poster_path")
        )

        image_url = None

        if poster_path:

            image_url = (
                "https://image.tmdb.org/t/p/"
                "w780"
                f"{poster_path}"
            )

        source_url = (
            f"https://www.themoviedb.org/tv/"
            f"{show_id}"
            if show_id
            else "https://www.themoviedb.org/"
        )

        event_text = (
            f"{title} first aired on "
            f"{historical_date.day} "
            f"{historical_date.strftime('%B')} "
            f"{historical_date.year}."
        )

        results.append(
            {
                "year": historical_date.year,
                "date": historical_date.isoformat(),
                "display_date": (
                    f"{historical_date.day} "
                    f"{historical_date.strftime('%B')} "
                    f"{historical_date.year}"
                ),
                "years_ago": years_ago,
                "source_category": "tv",
                "title": title,
                "event": event_text,
                "description": overview,
                "extract": "",
                "source_url": source_url,
                "image_url": image_url,
            }
        )

    return results


# ============================================================
# IGDB
# ============================================================

IGDB_CLIENT_ID = os.getenv(
    "IGDB_CLIENT_ID"
)

IGDB_CLIENT_SECRET = os.getenv(
    "IGDB_CLIENT_SECRET"
)

IGDB_TOKEN_URL = (
    "https://id.twitch.tv/oauth2/token"
)

IGDB_BASE_URL = (
    "https://api.igdb.com/v4"
)


_igdb_access_token = None
_igdb_token_expiry = 0


async def get_igdb_token(
    client: httpx.AsyncClient,
) -> str | None:

    global _igdb_access_token
    global _igdb_token_expiry

    if not IGDB_CLIENT_ID:
        return None

    if not IGDB_CLIENT_SECRET:
        return None

    # Reuse token while it is valid.
    if (
        _igdb_access_token
        and time.time()
        < _igdb_token_expiry - 60
    ):
        return _igdb_access_token

    response = await client.post(
        IGDB_TOKEN_URL,
        params={
            "client_id": IGDB_CLIENT_ID,
            "client_secret": IGDB_CLIENT_SECRET,
            "grant_type": "client_credentials",
        },
    )

    response.raise_for_status()

    data = response.json()

    token = data.get(
        "access_token"
    )

    expires_in = int(
        data.get(
            "expires_in",
            0,
        )
    )

    if not token:
        return None

    _igdb_access_token = token

    _igdb_token_expiry = (
        time.time()
        + expires_in
    )

    return token


async def fetch_gaming_events(
    target_date: date,
) -> list[dict[str, Any]]:

    if not IGDB_CLIENT_ID:
        print(
            "IGDB_CLIENT_ID not configured. "
            "Skipping gaming."
        )

        return []

    if not IGDB_CLIENT_SECRET:
        print(
            "IGDB_CLIENT_SECRET not configured. "
            "Skipping gaming."
        )

        return []

    events = []

    async with httpx.AsyncClient(
        timeout=TIMEOUT,
        headers={
            "User-Agent": USER_AGENT,
        },
    ) as client:

        token = await get_igdb_token(
            client
        )

        if not token:
            return []

        headers = {
            "Client-ID": IGDB_CLIENT_ID,
            "Authorization": (
                f"Bearer {token}"
            ),
            "User-Agent": USER_AGENT,
        }

        for years_ago in LOOKBACK_YEARS:

            historical_year = (
                target_date.year - years_ago
            )

            historical_date = date(
                historical_year,
                target_date.month,
                target_date.day,
            )

            try:

                results = (
                    await fetch_igdb_day(
                        client=client,
                        headers=headers,
                        historical_date=historical_date,
                        years_ago=years_ago,
                    )
                )

                events.extend(
                    results
                )

            except Exception as e:

                print(
                    "IGDB source error:",
                    e,
                )

    return events


async def fetch_igdb_day(
    client: httpx.AsyncClient,
    headers: dict[str, str],
    historical_date: date,
    years_ago: int,
) -> list[dict[str, Any]]:

    start_datetime = datetime(
        historical_date.year,
        historical_date.month,
        historical_date.day,
        tzinfo=timezone.utc,
    )

    end_datetime = (
        start_datetime
        + __import__(
            "datetime"
        ).timedelta(days=1)
    )

    start_timestamp = int(
        start_datetime.timestamp()
    )

    end_timestamp = int(
        end_datetime.timestamp()
    )

    query = f"""
fields
    date,
    game.name,
    game.summary,
    game.cover.url,
    game.url;
where
    date >= {start_timestamp}
    & date < {end_timestamp};
sort date asc;
limit 30;
"""

    response = await client.post(
        f"{IGDB_BASE_URL}/release_dates",
        headers=headers,
        content=query,
    )

    response.raise_for_status()

    release_dates = response.json()

    results = []

    seen_games = set()

    for release in release_dates:

        game = (
            release.get("game")
            or {}
        )

        title = (
            game.get("name")
            or ""
        ).strip()

        if not title:
            continue

        game_key = title.lower()

        if game_key in seen_games:
            continue

        seen_games.add(
            game_key
        )

        summary = (
            game.get("summary")
            or ""
        ).strip()

        game_url = (
            game.get("url")
            or "https://www.igdb.com/"
        )

        cover = (
            game.get("cover")
            or {}
        )

        image_url = None

        cover_url = cover.get(
            "url"
        )

        if cover_url:

            image_url = (
                cover_url
                .replace(
                    "t_thumb",
                    "t_1080p",
                )
            )

            if image_url.startswith(
                "//"
            ):
                image_url = (
                    "https:"
                    + image_url
                )

        event_text = (
            f"{title} had a game release "
            f"recorded on "
            f"{historical_date.day} "
            f"{historical_date.strftime('%B')} "
            f"{historical_date.year}."
        )

        results.append(
            {
                "year": historical_date.year,
                "date": historical_date.isoformat(),
                "display_date": (
                    f"{historical_date.day} "
                    f"{historical_date.strftime('%B')} "
                    f"{historical_date.year}"
                ),
                "years_ago": years_ago,
                "source_category": "gaming",
                "title": title,
                "event": event_text,
                "description": summary,
                "extract": "",
                "source_url": game_url,
                "image_url": image_url,
            }
        )

    return results


# ============================================================
# Combined sources
# ============================================================

async def fetch_additional_events(
    target_date: date,
) -> list[dict[str, Any]]:

    results = await asyncio.gather(
        fetch_sports_events(
            target_date
        ),
        fetch_music_events(
            target_date
        ),
        fetch_tmdb_events(
            target_date
        ),
        fetch_gaming_events(
            target_date
        ),
        return_exceptions=True,
    )

    combined = []

    for result in results:

        if isinstance(
            result,
            Exception,
        ):
            continue

        combined.extend(
            result
        )

    return combined
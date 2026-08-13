import html
import re
from datetime import date
from typing import Any

import httpx


WIKIMEDIA_URL = (
    "https://en.wikipedia.org/api/rest_v1/"
    "feed/onthisday/all/{month:02d}/{day:02d}"
)

TIMEOUT = 15

HEADERS = {
    "User-Agent": (
        "TelegramAutomations/1.0 "
        "(personal historical content project)"
    ),
    "Accept": "application/json",
}


async def fetch_today_events(
    target_date: date | None = None,
) -> list[dict[str, Any]]:

    target_date = target_date or date.today()

    url = WIKIMEDIA_URL.format(
        month=target_date.month,
        day=target_date.day,
    )

    async with httpx.AsyncClient(
        timeout=TIMEOUT,
        headers=HEADERS,
    ) as client:

        response = await client.get(url)
        response.raise_for_status()

        data = response.json()

    candidates = []

    # The "all" feed can contain several categories.
    # We deliberately collect everything and let Gemini
    # decide what is interesting.
    for category in (
        "selected",
        "events",
        "births",
        "deaths",
    ):

        for item in data.get(category, []):

            candidate = parse_event(
                item=item,
                category=category,
                target_date=target_date,
            )

            if candidate:
                candidates.append(candidate)

    return deduplicate_events(candidates)


def parse_event(
    item: dict[str, Any],
    category: str,
    target_date: date,
) -> dict[str, Any] | None:

    year = item.get("year")

    text = clean_text(
        item.get("text", "")
    )

    if year is None or not text:
        return None

    pages = item.get("pages") or []

    if not pages:
        return None

    page = pages[0]

    titles = page.get("titles") or {}

    title = clean_text(
        titles.get("display")
        or titles.get("canonical")
        or page.get("title")
        or ""
    )

    description = clean_text(
        page.get("description")
        or ""
    )

    extract = clean_text(
        page.get("extract")
        or ""
    )

    content_urls = page.get(
        "content_urls",
        {},
    )

    source_url = (
        content_urls
        .get("desktop", {})
        .get("page")
    )

    thumbnail = page.get(
        "thumbnail"
    ) or {}

    original_image = page.get(
        "originalimage"
    ) or {}

    image_url = (
        original_image.get("source")
        or thumbnail.get("source")
    )

    year = int(year)

    # Wikimedia can represent BCE years using
    # negative numbers.
    if year < 0:

        historical_year = (
            f"{abs(year) + 1} BCE"
        )

        years_ago = (
            target_date.year + abs(year)
        )

    elif year == 0:

        historical_year = "1 BCE"

        years_ago = (
            target_date.year + 1
        )

    else:

        historical_year = str(year)

        years_ago = (
            target_date.year - year
        )

    display_date = (
        f"{target_date.day} "
        f"{target_date.strftime('%B')} "
        f"{historical_year}"
    )

    return {
        "year": year,
        "date": (
            f"{historical_year}-"
            f"{target_date.month:02d}-"
            f"{target_date.day:02d}"
        ),
        "display_date": display_date,
        "years_ago": years_ago,
        "source_category": category,
        "title": title,
        "event": text,
        "description": description,
        "extract": extract,
        "source_url": source_url,
        "image_url": image_url,
    }


def clean_text(value: str) -> str:

    if not value:
        return ""

    value = html.unescape(value)

    # Remove HTML tags properly.
    value = re.sub(
        r"<[^>]+>",
        "",
        value,
    )

    value = html.unescape(value)

    # Normalize whitespace.
    value = " ".join(
        value.split()
    )

    return value.strip()


def deduplicate_events(
    events: list[dict[str, Any]],
) -> list[dict[str, Any]]:

    seen = set()
    unique = []

    for event in events:

        key = (
            event["year"],
            event["title"].lower().strip(),
            event["event"].lower().strip(),
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(event)

    return unique
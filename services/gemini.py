import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
from google.genai import types


GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite",
)

client = genai.Client(
    api_key=GEMINI_API_KEY
)


EVENT_DISCOVERY_SCHEMA = {
    "type": "object",
    "properties": {
        "events": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string"
                    },
                    "year": {
                        "type": "integer"
                    },
                    "category": {
                        "type": "string"
                    },
                    "event": {
                        "type": "string"
                    },
                    "source_url": {
                        "type": "string"
                    },
                    "confidence": {
                        "type": "integer"
                    }
                },
                "required": [
                    "title",
                    "year",
                    "category",
                    "event",
                    "source_url",
                    "confidence"
                ]
            }
        }
    },
    "required": [
        "events"
    ]
}


RANKING_SCHEMA = {
    "type": "object",
    "properties": {
        "selected_events": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "candidate_index": {
                        "type": "integer"
                    },
                    "reason": {
                        "type": "string"
                    },
                    "score": {
                        "type": "integer"
                    }
                },
                "required": [
                    "candidate_index",
                    "reason",
                    "score"
                ]
            }
        }
    },
    "required": [
        "selected_events"
    ]
}


async def discover_events(
    date_text: str,
) -> list[dict]:

    prompt = f"""
You are researching content for a daily "On This Day"
social media account.

Today's date is:

{date_text}

Find genuinely interesting events that happened on this
EXACT calendar date in previous years.

IMPORTANT:

The event must have happened specifically on this month
and day.

Do NOT include:
- events that merely happened during the same month
- events that happened a few days before or after
- ongoing events unless something specific happened on this date
- anniversaries that are not tied to an actual event date
- vague historical claims

Search broadly across ALL categories.

Possible categories include:
- History
- World events
- India
- Sports
- Football
- Cricket
- Olympics
- Music
- Movies
- Television
- Gaming
- Technology
- Science
- Space
- Business
- Internet culture
- Cars
- Aviation
- Books
- Awards
- Famous people
- Weird or unusual events

Do not favor history.

Look for events that would make a person think:

"I didn't know that happened on this day."

For every candidate provide:
- exact event title
- original event year
- category
- concise factual description
- source URL
- confidence from 1 to 10

Only return events for which you can find a reliable
source supporting the exact date.

Return at least 15 candidates if enough genuine candidates
exist.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=EVENT_DISCOVERY_SCHEMA,
            tools=[
                types.Tool(
                    google_search=types.GoogleSearch()
                )
            ],
        ),
    )

    data = json.loads(
        response.text
    )

    return data.get(
        "events",
        []
    )


async def rank_events(
    events: list[dict],
) -> list[dict]:

    if not events:
        return []

    candidates_text = []

    for index, event in enumerate(
        events
    ):

        candidates_text.append(
            f"""
CANDIDATE {index}

Title:
{event.get("title")}

Year:
{event.get("year")}

Category:
{event.get("category")}

Event:
{event.get("event")}

Source:
{event.get("source_url")}

Research confidence:
{event.get("confidence")}
"""
        )

    prompt = f"""
You are the editor for a social media account called
"On This Day".

You have been given historical events that have already
been researched for the exact calendar date.

Your job is to select the THREE strongest candidates.

The account is NOT limited to history.

A great candidate can come from:
sports, music, movies, gaming, technology, science,
space, business, India, internet culture, famous people,
weird events, or traditional history.

Choose events that are:

1. Genuinely interesting.
2. Broadly understandable.
3. Strong enough to make a good Twitter/X post.
4. Suitable for a Reddit post.
5. Supported by a source.
6. Distinct from one another when possible.

Avoid:
- boring administrative events
- obscure events with no interesting angle
- generic deaths/births unless the person is highly notable
- events that are only interesting because they are old
- duplicate or near-duplicate events

IMPORTANT:

Do NOT change facts.

Do NOT change the event year.

Do NOT invent details.

Select exactly three candidates.

Here are the candidates:

{"".join(candidates_text)}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RANKING_SCHEMA,
        ),
    )

    data = json.loads(
        response.text
    )

    selected = []

    for item in data.get(
        "selected_events",
        []
    ):

        index = item.get(
            "candidate_index"
        )

        if (
            isinstance(index, int)
            and 0 <= index < len(events)
        ):

            event = events[index].copy()

            event["score"] = item.get(
                "score",
                0
            )

            event["reason"] = item.get(
                "reason",
                ""
            )

            selected.append(
                event
            )

    return selected[:3]
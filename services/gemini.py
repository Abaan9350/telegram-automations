import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite",
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


CATEGORIES = [
    "History",
    "Sports",
    "Music",
    "Movies & TV",
    "Gaming",
    "Technology",
    "Science",
    "Space",
    "Business",
    "India",
    "Internet",
    "People",
    "Motorsport",
    "Aviation",
    "Books",
    "Awards",
    "Weird",
]


RANKING_SCHEMA = {
    "type": "object",
    "properties": {
        "selected_events": {
            "type": "array",
            "minItems": 3,
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    "candidate_index": {
                        "type": "integer",
                    },
                    "category": {
                        "type": "string",
                        "enum": CATEGORIES,
                    },
                    "reason": {
                        "type": "string",
                    },
                    "score": {
                        "type": "integer",
                    },
                },
                "required": [
                    "candidate_index",
                    "category",
                    "reason",
                    "score",
                ],
            },
        },
    },
    "required": [
        "selected_events",
    ],
}


async def rank_events(
    events: list[dict],
) -> list[dict]:

    if len(events) < 3:
        return events

    candidates = []

    for index, event in enumerate(events):

        candidates.append(
            f"""
CANDIDATE {index}

Title:
{event.get("title", "")}

Year:
{event.get("year", "")}

Historical date:
{event.get("display_date", "")}

Original source category:
{event.get("source_category", "")}

Event:
{event.get("event", "")}

Description:
{event.get("description", "")}

Source:
{event.get("source_url", "")}

Image available:
{"Yes" if event.get("image_url") else "No"}
"""
        )

    candidates_text = "\n".join(
        candidates
    )

    prompt = f"""
You are the editor for a social media account called
"On This Day".

You have a large collection of events that happened on
the exact calendar date being researched.

Your job is to select EXACTLY THREE events that would make
excellent social media posts.

The account is NOT a history account.

It covers interesting events from EVERY domain.

AVAILABLE CATEGORIES:

{", ".join(CATEGORIES)}

CATEGORY RULES:

Every selected event MUST receive exactly one category
from the list above.

Do NOT use "General".

Choose the category based on the actual subject of the
event, not the source it came from.

Examples:

A football match:
Sports

A video game release:
Gaming

An album release:
Music

A movie premiere:
Movies & TV

A spacecraft launch:
Space

A scientific discovery:
Science

A company/product launch:
Technology or Business

An event specifically connected to India:
India

A famous person's birth/death:
People

A Formula 1 race:
Motorsport

An aircraft milestone:
Aviation

A strange or bizarre historical event:
Weird

A war or major historical event:
History

A Grammy/Oscar/major award:
Awards

SELECTION RULES:

Prioritize events that make someone think:

"I didn't know that happened on this day."

Look for:

- major firsts
- famous achievements
- surprising facts
- iconic moments
- major launches
- important discoveries
- famous sports moments
- famous music/movie/gaming milestones
- unusual events
- culturally significant moments
- events with strong storytelling potential

Avoid:

- mundane events
- extremely obscure events
- generic births/deaths
- events with little social-media potential
- duplicate events
- near-duplicate events

CATEGORY DIVERSITY:

Try to select events from different categories.

For example, if there are strong candidates from
Gaming, Sports and Music, prefer those over selecting
three History events.

However, NEVER sacrifice a dramatically better event
just to force category diversity.

FACTUAL ACCURACY:

The candidates have already been researched.

Do NOT:

- invent facts
- change dates
- change years
- invent sources
- combine two candidates
- add information not present in the candidates

Select candidates only by their original candidate index.

Return EXACTLY THREE candidates.

For every selected candidate provide:

candidate_index:
The original candidate number.

category:
Exactly one category from the allowed list.

reason:
A short explanation of why this event is interesting.

score:
A score from 1 to 100 representing social-media potential.

CANDIDATES:

{candidates_text}
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
        [],
    ):

        index = item.get(
            "candidate_index"
        )

        if not isinstance(index, int):
            continue

        if not 0 <= index < len(events):
            continue

        event = events[index].copy()

        category = item.get(
            "category"
        )

        if category not in CATEGORIES:
            category = infer_fallback_category(
                event
            )

        event["category"] = category

        event["reason"] = item.get(
            "reason",
            "",
        )

        event["score"] = item.get(
            "score",
            0,
        )

        selected.append(event)

    if len(selected) < 3:

        fallback = events[:3]

        for event in fallback:

            event.setdefault(
                "category",
                infer_fallback_category(event),
            )

            event.setdefault(
                "reason",
                "",
            )

            event.setdefault(
                "score",
                0,
            )

        return fallback

    return selected[:3]


def infer_fallback_category(
    event: dict,
) -> str:

    text = (
        f"{event.get('title', '')} "
        f"{event.get('event', '')} "
        f"{event.get('description', '')}"
    ).lower()

    if any(
        word in text
        for word in [
            "football",
            "soccer",
            "cricket",
            "olympic",
            "tennis",
            "basketball",
            "championship",
            "match",
            "player",
            "athlete",
        ]
    ):
        return "Sports"

    if any(
        word in text
        for word in [
            "album",
            "song",
            "singer",
            "music",
            "band",
            "concert",
            "recording",
        ]
    ):
        return "Music"

    if any(
        word in text
        for word in [
            "video game",
            "game console",
            "playstation",
            "xbox",
            "nintendo",
            "arcade",
        ]
    ):
        return "Gaming"

    if any(
        word in text
        for word in [
            "film",
            "movie",
            "television",
            "tv series",
            "actor",
            "actress",
        ]
    ):
        return "Movies & TV"

    if any(
        word in text
        for word in [
            "nasa",
            "apollo",
            "spacecraft",
            "astronaut",
            "moon landing",
            "orbit",
        ]
    ):
        return "Space"

    if any(
        word in text
        for word in [
            "scientist",
            "discovery",
            "experiment",
            "research",
            "theory",
        ]
    ):
        return "Science"

    if any(
        word in text
        for word in [
            "internet",
            "website",
            "online",
            "social media",
            "viral",
        ]
    ):
        return "Internet"

    if any(
        word in text
        for word in [
            "computer",
            "software",
            "technology",
            "iphone",
            "microsoft",
            "apple",
            "google",
        ]
    ):
        return "Technology"

    if any(
        word in text
        for word in [
            "formula 1",
            "formula one",
            "f1",
            "grand prix",
            "racing",
        ]
    ):
        return "Motorsport"

    if any(
        word in text
        for word in [
            "aircraft",
            "airplane",
            "aviation",
            "flight",
            "pilot",
        ]
    ):
        return "Aviation"

    if any(
        word in text
        for word in [
            "book",
            "novel",
            "author",
            "published",
        ]
    ):
        return "Books"

    if any(
        word in text
        for word in [
            "oscar",
            "grammy",
            "emmy",
            "award",
            "prize",
        ]
    ):
        return "Awards"

    if any(
        word in text
        for word in [
            "india",
            "indian",
            "delhi",
            "mumbai",
            "kolkata",
            "chennai",
        ]
    ):
        return "India"

    if any(
        word in text
        for word in [
            "company",
            "corporation",
            "business",
            "founded",
            "acquired",
        ]
    ):
        return "Business"

    if any(
        word in text
        for word in [
            "born",
            "died",
            "death",
            "birth",
        ]
    ):
        return "People"

    return "History"
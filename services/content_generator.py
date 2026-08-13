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


CONTENT_SCHEMA = {
    "type": "object",
    "properties": {
        "twitter_body": {
            "type": "string",
        },
        "reddit_subreddit": {
            "type": "string",
        },
        "reddit_title": {
            "type": "string",
        },
        "reddit_body": {
            "type": "string",
        },
    },
    "required": [
        "twitter_body",
        "reddit_subreddit",
        "reddit_title",
        "reddit_body",
    ],
}


ALLOWED_SUBREDDITS = [
    "r/todayilearned",
    "r/history",
    "r/AskHistorians",
    "r/science",
    "r/technology",
    "r/gaming",
    "r/Music",
    "r/movies",
    "r/tv",
    "r/sports",
    "r/football",
    "r/soccer",
    "r/cricket",
    "r/space",
    "r/interestingasfuck",
    "r/interesting",
]


async def generate_post_content(
    event: dict,
) -> dict:

    title = event.get(
        "title",
        "",
    )

    event_text = event.get(
        "event",
        "",
    )

    description = event.get(
        "description",
        "",
    )

    extract = event.get(
        "extract",
        "",
    )

    category = event.get(
        "category",
        "History",
    )

    display_date = event.get(
        "display_date",
        "",
    )

    source_url = event.get(
        "source_url",
        "",
    )

    prompt = f"""
You are creating social-media content for an
"On This Day" account.

The selected event is:

Title:
{title}

Date:
{display_date}

Category:
{category}

Event:
{event_text}

Description:
{description}

Additional source information:
{extract}

Source:
{source_url}


YOUR TASK

Create:

1. A Twitter/X post.

2. A Reddit post.

The user will manually copy and publish both posts.

FACTUAL RULES

Only use information supported by the supplied event.

Do NOT invent:

- dates
- people
- statistics
- quotes
- locations
- causes
- consequences
- historical details

You may make the wording engaging, but the facts must
remain faithful to the supplied event.

Do not claim that something was the "first ever" unless
the supplied information explicitly supports that claim.

Do not exaggerate.

Do not use fake quotes.

Do not mention that you are an AI.

TWITTER

Write a concise, engaging Twitter/X post.

The post should:

- immediately communicate what happened
- mention the date or "X years ago"
- have a natural human tone
- encourage curiosity
- preferably stay comfortably below 280 characters
- use at most 2 relevant emojis
- avoid hashtags unless one is genuinely useful

Do NOT include:

"Source:"
"Reddit:"
"Twitter:"
or explanatory notes.

REDDIT

Choose the most appropriate subreddit from this list:

{", ".join(ALLOWED_SUBREDDITS)}

Choose based on the actual event.

Prefer a specialized subreddit when the event clearly
belongs there.

Use r/todayilearned for a general surprising historical
fact when appropriate.

Use r/interesting or r/interestingasfuck only when the
event genuinely fits that type of content.

Do not recommend a subreddit simply because its name
contains the event's category.

The Reddit title should be clear and factual.

The Reddit body should:

- explain the event naturally
- provide enough context to understand why it matters
- encourage discussion where appropriate
- avoid unnecessary clickbait
- not repeat the title word-for-word
- not include fake questions

Do NOT include Markdown headings such as:

"Title:"
"Body:"
"Source:"

Those fields are already separated by the application.

Return ONLY valid JSON matching the requested schema.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CONTENT_SCHEMA,
        ),
    )

    data = json.loads(
        response.text
    )

    twitter_body = (
        data.get("twitter_body")
        or ""
    ).strip()

    reddit_subreddit = (
        data.get("reddit_subreddit")
        or "r/todayilearned"
    ).strip()

    reddit_title = (
        data.get("reddit_title")
        or ""
    ).strip()

    reddit_body = (
        data.get("reddit_body")
        or ""
    ).strip()

    # Safety check.
    # If Gemini returns an unsupported subreddit,
    # fall back to TIL.
    normalized_subreddit = (
        reddit_subreddit.lower()
    )

    valid_subreddit = None

    for subreddit in ALLOWED_SUBREDDITS:

        if (
            subreddit.lower()
            == normalized_subreddit
        ):
            valid_subreddit = subreddit
            break

    if not valid_subreddit:
        valid_subreddit = (
            "r/todayilearned"
        )

    return {
        "twitter_body": twitter_body,
        "reddit_subreddit": valid_subreddit,
        "reddit_title": reddit_title,
        "reddit_body": reddit_body,
    }
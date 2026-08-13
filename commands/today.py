import os
from datetime import datetime
from io import BytesIO
from zoneinfo import ZoneInfo

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
)
from telegram.ext import ContextTypes

from commands import command

from services.historical_events import (
    fetch_today_events,
)

from services.gemini import (
    rank_events,
)

from services.content_generator import (
    generate_post_content,
)

from services.media import (
    download_image,
)


TIMEZONE = os.getenv(
    "TIMEZONE",
    "Asia/Kolkata",
)


CATEGORY_EMOJIS = {
    "History": "🌍",
    "Sports": "⚽",
    "Music": "🎵",
    "Movies & TV": "🎬",
    "Gaming": "🎮",
    "Technology": "💻",
    "Science": "🔬",
    "Space": "🚀",
    "Business": "💰",
    "India": "🇮🇳",
    "Internet": "🌐",
    "People": "👤",
    "Motorsport": "🏎️",
    "Aviation": "✈️",
    "Books": "📚",
    "Awards": "🏆",
    "Weird": "😂",
}


def get_today() -> datetime:

    return datetime.now(
        ZoneInfo(TIMEZONE)
    )


def format_age(
    years_ago: int,
) -> str:

    if years_ago == 1:
        return "1 year ago"

    return f"{years_ago} years ago"


def format_category(
    category: str,
) -> str:

    emoji = CATEGORY_EMOJIS.get(
        category,
        "📌",
    )

    return f"{emoji} {category}"


def build_candidate_message(
    events: list[dict],
    today: datetime,
) -> str:

    lines = [
        "🔥 TODAY'S PICKS",
        "",
        f"📅 {today.strftime('%d %B %Y')}",
        "",
    ]

    for index, event in enumerate(
        events,
        1,
    ):

        category = event.get(
            "category",
            "History",
        )

        lines.extend(
            [
                f"{index}️⃣ {event['title']}",
                (
                    f"🕰️ "
                    f"{format_age(event['years_ago'])}"
                ),
                (
                    f"🏷️ "
                    f"{format_category(category)}"
                ),
                f"📚 {event['event']}",
                "",
            ]
        )

    lines.append(
        "👇 Choose an event:"
    )

    return "\n".join(lines)


def build_keyboard(
    events: list[dict],
) -> InlineKeyboardMarkup:

    buttons = []

    for index, _ in enumerate(
        events,
        1,
    ):

        buttons.append(
            InlineKeyboardButton(
                f"{index}️⃣",
                callback_data=(
                    f"today_select:{index - 1}"
                ),
            )
        )

    return InlineKeyboardMarkup(
        [buttons]
    )


def build_post_preview(
    event: dict,
    content: dict,
) -> str:

    title = event.get(
        "title",
        "Unknown event",
    )

    display_date = event.get(
        "display_date",
        "",
    )

    category = event.get(
        "category",
        "History",
    )

    source_url = event.get(
        "source_url"
    )

    lines = [
        "🔥 READY TO POST",
        "",
        f"📌 {title}",
        f"📅 {display_date}",
        (
            f"🏷️ "
            f"{format_category(category)}"
        ),
        "",
        "━━━━━━━━━━━━━━━━━━",
        "🐦 TWITTER / X",
        "━━━━━━━━━━━━━━━━━━",
        "",
        content["twitter_body"],
        "",
        "━━━━━━━━━━━━━━━━━━",
        "🔴 REDDIT",
        "━━━━━━━━━━━━━━━━━━",
        "",
        (
            f"📍 "
            f"{content['reddit_subreddit']}"
        ),
        "",
        "TITLE:",
        content["reddit_title"],
        "",
        "BODY:",
        content["reddit_body"],
    ]

    if source_url:

        lines.extend(
            [
                "",
                "━━━━━━━━━━━━━━━━━━",
                "🔗 SOURCE",
                source_url,
            ]
        )

    return "\n".join(lines)


@command(
    "today",
    "Find interesting events from this day",
)
async def today(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    message = update.effective_message

    try:

        today = get_today()

        await message.reply_text(
            "🔎 Searching today's "
            "historical events..."
        )

        events = await fetch_today_events(
            today.date()
        )

        if not events:

            await message.reply_text(
                "😕 I couldn't find any "
                "events for today."
            )

            return

        await message.reply_text(
            f"🔎 Found {len(events)} "
            "historical candidates.\n\n"
            "🧠 Gemini is choosing the "
            "three most interesting ones..."
        )

        top_events = await rank_events(
            events
        )

        if not top_events:

            await message.reply_text(
                "😕 I couldn't select "
                "suitable events."
            )

            return

        context.user_data[
            "today_events"
        ] = top_events

        await message.reply_text(
            build_candidate_message(
                top_events,
                today,
            ),
            reply_markup=build_keyboard(
                top_events
            ),
        )

    except Exception as e:

        print(
            f"today error: {e}"
        )

        await message.reply_text(
            "⚠️ Couldn't retrieve "
            "today's events.\n\n"
            f"Error: {e}"
        )


async def today_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    try:

        index = int(
            query.data.split(":")[1]
        )

        events = context.user_data.get(
            "today_events"
        )

        if not events:

            await query.edit_message_text(
                "⚠️ These results have expired.\n\n"
                "Please run /today again."
            )

            return

        if index < 0 or index >= len(events):

            await query.edit_message_text(
                "⚠️ Invalid selection."
            )

            return

        selected = events[index]

        # ----------------------------------------------------
        # Generate Twitter + Reddit content
        # ----------------------------------------------------

        await query.edit_message_text(
            "🧠 Generating Twitter and "
            "Reddit posts..."
        )

        content = (
            await generate_post_content(
                selected
            )
        )

        # ----------------------------------------------------
        # Build preview
        # ----------------------------------------------------

        preview = build_post_preview(
            selected,
            content,
        )

        await query.message.reply_text(
            preview,
            disable_web_page_preview=True,
        )

        # ----------------------------------------------------
        # Download image
        # ----------------------------------------------------

        image_url = selected.get(
            "image_url"
        )

        if image_url:

            image_bytes, extension = (
                await download_image(
                    image_url
                )
            )

            if image_bytes:

                caption = (
                    f"🖼️ Image for:\n"
                    f"{selected.get('title', '')}\n\n"
                    f"Source:\n"
                    f"{image_url}"
                )

                photo_file = InputFile(
                    BytesIO(image_bytes),
                    filename=f"event.{extension}",
                )

                await query.message.reply_photo(
                    photo=photo_file,
                    caption=caption,
                )

            else:

                await query.message.reply_text(
                    "⚠️ I couldn't download "
                    "the source image.\n\n"
                    f"🖼️ Image URL:\n"
                    f"{image_url}"
                )

        else:

            await query.message.reply_text(
                "⚠️ No image was available "
                "for this event."
            )

        # ----------------------------------------------------
        # Final confirmation
        # ----------------------------------------------------

        await query.message.reply_text(
            "✅ Posting package ready.\n\n"
            "🐦 Copy the Twitter text.\n"
            "🔴 Copy the Reddit title and body.\n"
            "🖼️ Download/save the image above.\n\n"
            "Nothing has been posted automatically."
        )

    except Exception as e:

        print(
            f"today_callback error: {e}"
        )

        try:

            await query.edit_message_text(
                "⚠️ Something went wrong while "
                "generating the posting package.\n\n"
                f"Error: {e}"
            )

        except Exception:

            await query.message.reply_text(
                "⚠️ Something went wrong while "
                "generating the posting package.\n\n"
                f"Error: {e}"
            )
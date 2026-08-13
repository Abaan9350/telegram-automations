import os
from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from commands import command

from services.historical_events import (
    fetch_today_events,
)

from services.gemini import (
    rank_events,
)


TIMEZONE = os.getenv(
    "TIMEZONE",
    "Asia/Kolkata",
)


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

        lines.extend(
            [
                f"{index}️⃣ {event['title']}",
                f"🕰️ {format_age(event['years_ago'])}",
                f"🏷️ {event.get('category', 'General')}",
                f"📚 {event['event']}",
                "",
            ]
        )

    lines.extend(
        [
            "👇 Choose an event:",
        ]
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

        # Store the three selected events
        # for the Telegram buttons.
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

        title = selected.get(
            "title",
            "Unknown event",
        )

        category = selected.get(
            "category",
            "General",
        )

        source_url = selected.get(
            "source_url"
        )

        image_url = selected.get(
            "image_url"
        )

        lines = [
            "✅ EVENT SELECTED",
            "",
            f"📌 {title}",
            "",
            f"📅 {selected.get('display_date', '')}",
            "",
            f"🏷️ {category}",
            "",
            f"📚 {selected.get('event', '')}",
        ]

        if selected.get("reason"):

            lines.extend(
                [
                    "",
                    "🧠 Why Gemini picked it:",
                    selected["reason"],
                ]
            )

        if source_url:

            lines.extend(
                [
                    "",
                    "🔗 Source:",
                    source_url,
                ]
            )

        if image_url:

            lines.extend(
                [
                    "",
                    "🖼️ Image:",
                    image_url,
                ]
            )

        await query.edit_message_text(
            "\n".join(lines),
            disable_web_page_preview=False,
        )

    except Exception as e:

        print(
            f"today_callback error: {e}"
        )

        await query.edit_message_text(
            "⚠️ Something went wrong while "
            "selecting that event.\n\n"
            f"Error: {e}"
        )
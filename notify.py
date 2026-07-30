import os

ADMIN_ID = int(os.environ["ADMIN_ID"])


async def notify_admin(context, user, command_name, is_new):
    # Only notify for brand new users
    if not is_new:
        return

    username = f"@{user.username}" if user.username else "No username"
    first_name = user.first_name or "Unknown"

    message = (
        "🎉 <b>New User!</b>\n\n"
        f"👤 <b>Name:</b> {first_name}\n"
        f"📛 <b>Username:</b> {username}\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
        f"💬 <b>First Command:</b> {command_name}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=message,
        parse_mode="HTML",
    )
import os
from telegram import Update
from telegram.ext import ContextTypes

from . import command
from users import get_all_users

ADMIN_ID = int(os.environ["ADMIN_ID"])


@command("users")
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized.")
        return

    users = get_all_users()

    if not users:
        await update.message.reply_text("No users found.")
        return

    message = f"👥 Total Users: {len(users)}\n\n"

    for user_id, username, first_name, last_seen in users:
        username = f"@{username}" if username else "No username"
        first_name = first_name or "Unknown"

        message += (
            f"• {first_name} ({username})\n"
            f"ID: {user_id}\n\n"
        )

    await update.message.reply_text(message[:4000])
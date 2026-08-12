import os
import re
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from commands import command
from services.google_sheets import append_transaction, undo_last_expense


TRANSACTION_REGEX = re.compile(
    r"^/(expense|income)\s+(.+?)\s+([1-9]\d*(?:\.\d{1,2})?)(?:\s+(.+))?$",
    re.IGNORECASE,
)


def is_admin(update: Update) -> bool:
    return update.effective_user.id == int(os.environ["ADMIN_ID"])


async def handle_transaction(
    update: Update,
    transaction_type: str,
):
    if not is_admin(update):
        return

    text = update.effective_message.text.strip()
    match = TRANSACTION_REGEX.match(text)

    if not match:
        await update.effective_message.reply_text(
            "❌ Invalid format.\n\n"
            "Examples:\n"
            "/expense chicken 200\n"
            "/expense shoes 260 size 10\n"
            "/income salary 41667"
        )
        return

    _, item, amount, description = match.groups()

    append_transaction(
        date=datetime.now().strftime("%d %b %y").lstrip("0"),
        item=item.strip(),
        amount=amount,
        transaction_type=transaction_type,
        description=(description or "").strip(),
    )

    await update.effective_message.reply_text(
        f"✅ {transaction_type.capitalize()} added: ₹{amount} for {item.strip()}"
    )


@command("expense", "Add an expense")
async def expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.effective_message.reply_text(
            "⛔ You are not authorized to use this command."
        )
        return

    await handle_transaction(update, "expense")


@command("income", "Add income")
async def income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.effective_message.reply_text(
            "⛔ You are not authorized to use this command."
        )
        return

    await handle_transaction(update, "income")

@command("undoexpense", "Undo the most recent expense")
async def undoexpense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.effective_message.reply_text(
            "⛔ You are not authorized to use this command."
        )
        return

    removed = undo_last_expense()

    if removed:
        await update.effective_message.reply_text(
            "✅ Last expense has been removed."
        )
    else:
        await update.effective_message.reply_text(
            "ℹ️ No expense found to undo."
        )
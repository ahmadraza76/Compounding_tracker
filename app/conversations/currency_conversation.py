# app/conversations/currency_conversation.py
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from app.utils.data_utils import update_user_data, get_user_data
from app.config.constants import CURRENCY_CHANGE
from app.config.messages import MESSAGES

async def handle_currency_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process currency symbol input."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")
    currency = update.message.text.strip()

    if not currency or len(currency) > 5:
        await update.message.reply_text(
            "❌ Please enter a valid currency symbol between 1 and 5 characters.",
            parse_mode="Markdown"
        )
        return CURRENCY_CHANGE

    update_user_data(user_id, {
        "currency": currency,
        "awaiting": None
    })

    await update.message.reply_text(
        f"✅ Currency symbol successfully set to {currency}!\nUse /settings to view your settings.",
        parse_mode="Markdown"
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel currency setting process."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")

    update_user_data(user_id, {"awaiting": None})

    await update.message.reply_text(
        MESSAGES[language]["cancel"],
        parse_mode="Markdown"
    )

    return ConversationHandler.END
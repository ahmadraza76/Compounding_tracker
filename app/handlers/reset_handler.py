# app/handlers/reset_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.utils.data_utils import get_user_data
from app.config.messages import MESSAGES

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Initiate data reset process with confirmation."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")

    keyboard = [
        [InlineKeyboardButton("✅ Yes" if language == "en" else "✅ हाँ", callback_data="confirm_reset_")],
        [InlineKeyboardButton("❌ No" if language == "en" else "❌ नहीं", callback_data="cancel_reset_")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        MESSAGES[language]["reset_prompt"],
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
